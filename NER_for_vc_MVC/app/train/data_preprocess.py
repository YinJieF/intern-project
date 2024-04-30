# Modify the make look up table when number of tag is changed
# Modify the label when the number of tag is changed
import keras
import pickle
import numpy as np
import pandas as pd
from time import time
import tensorflow as tf
from collections import Counter
from google.cloud import bigquery
from datasets import Dataset, DatasetDict
from sklearn.model_selection import train_test_split
from app.credentials.set_credential import set_credential


def get_bq_tables(dataset_id):
    credentials = set_credential()
    client = bigquery.Client(credentials=credentials)
    tables = client.list_tables(dataset_id)
    datasets = []
    for table in tables:
        datasets.append(table.table_id)
    return datasets

# read the (original) data from the bigquery
def read_bq(project_id, dataset_id, table_id, bigquery_client, size):
    query = f"""
        SELECT *
        FROM {project_id}.{dataset_id}.{table_id}
        WHERE extract_id < {size}
    """
    a  = time()
    query_job = bigquery_client.query(query)
    # Convert the result into a Pandas DataFrame
    df = query_job.to_dataframe()
    b = time()
    print(f"Time to read the data: {b-a}")
    return df

def make_tag_lookup_table():
    ner_labels = ["[PAD]", "N", "M", "B-PER", "I-PER", "other"]
    return dict(zip(range(len(ner_labels)), ner_labels))

def count_vocab(dataset_dict):
    all_tokens_array = np.concatenate([np.array(tokens) for tokens in dataset_dict["train"]["token"]])

    counter = Counter(all_tokens_array)

    vocab_size = 20000

    # We only take (vocab_size - 2) most common words from the training data since
    # the `StringLookup` class uses 2 additional tokens - one denoting an unknown
    # token and another one denoting a masking token
    vocabulary = [token for token, count in counter.most_common(vocab_size - 2)]

    # Save the list to a file
    with open('./app/train/resources/vocabulary.pkl', 'wb') as f:
        pickle.dump(vocabulary, f)

    # The StringLookup class will convert tokens to token IDs
    lookup_layer = keras.layers.StringLookup(vocabulary=vocabulary)
    return lookup_layer

def dt_to_df(dataset_dict):
    def export_to_file(export_file_path, data):
        with open(export_file_path, "w") as f:
            for record in data:
                ner_tags = record["self_tag"]
                tokens = record["token"]
                if len(tokens) > 0:
                    f.write(str(len(tokens)) + "\t" + "\t".join(tokens) + "\t"  + "\t".join(map(str, ner_tags)) + "\n")
    export_to_file("./app/train/resources/crime_train.txt", dataset_dict['train'])
    export_to_file("./app/train/resources/crime_val.txt", dataset_dict['test'])
    train_data = tf.data.TextLineDataset("./app/train/resources/crime_train.txt")
    val_data = tf.data.TextLineDataset("./app/train/resources/crime_val.txt")

    return train_data, val_data

def map_record_to_training_data(record):
    record = tf.strings.split(record, sep="\t")
    length = tf.strings.to_number(record[0], out_type=tf.int32)
    tokens = record[1 : length + 1]
    tags = record[length + 1 :]
    tags = tf.strings.to_number(tags, out_type=tf.int64)
    tags += 1
    return tokens, tags

def data_preprocessing(dataset, batch_size):
    # Eliminate all the CH (punctuation)
    dataset = dataset[dataset['tag_underthesea'] != 'CH']
    
    # Define the mapping
    label_map = {"N": 0, "M": 1, "B-PER": 2, "I-PER": 3, "other": 4}
    
    # Replace numeric labels with NER labels
    dataset_copy = dataset.copy()
    dataset_copy['self_label'] = dataset_copy['self_label'].map(label_map)
    dataset = dataset_copy
    dataset = dataset.sort_values(by='sequence')
    # Grouping the dataset by 'extract_id' and aggregating the 'text' and 'self_label' columns into lists
    grouped_data = dataset.groupby('extract_id').agg({'text': list, 'self_label': list}).reset_index()
    
    # Filter out sequences longer than 512 tokens
    grouped_data['sequence_length'] = grouped_data['text'].apply(len)
    grouped_data = grouped_data[grouped_data['sequence_length'] <= 512]
    
    # Convert grouped data into a dictionary
    dataset_dict = {
        'id': grouped_data['extract_id'].tolist(),
        'token': grouped_data['text'].tolist(),
        'self_tag': grouped_data['self_label'].tolist()
    }
    
    # Convert the dictionary to a DataFrame
    dataset_df = pd.DataFrame(dataset_dict)
    
    # Split data into train and test sets
    train_df, test_df = train_test_split(dataset_df, test_size=0.2, random_state=42)
    
    # Create train and test datasets
    train_dataset = Dataset.from_pandas(train_df)
    test_dataset = Dataset.from_pandas(test_df)
    
    # Construct DatasetDict
    dataset_dict = DatasetDict({'train': train_dataset, 'test': test_dataset})
    lookup_layer = count_vocab(dataset_dict)
    train_data, val_data = dt_to_df(dataset_dict)
    train_dataset = (
        train_data.map(map_record_to_training_data)
        .map(lambda x, y: (lookup_layer(x), y))
        .padded_batch(batch_size)
    )
    val_dataset = (
        val_data.map(map_record_to_training_data)
        .map(lambda x, y: (lookup_layer(x), y))
        .padded_batch(batch_size)
    )

    return train_dataset, val_dataset

def load_data(PROJECT_ID, DATASET_ID, TABLE_ID, size):
    credentials = set_credential()
    bigquery_client = bigquery.Client(credentials=credentials,
                                      project=PROJECT_ID)
    
    df = read_bq(PROJECT_ID, DATASET_ID, TABLE_ID, bigquery_client, size)
    
    df = data_preprocessing(df, batch_size = 16)

    return df