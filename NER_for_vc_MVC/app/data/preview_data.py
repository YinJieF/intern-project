from time import time
from google.cloud import bigquery
from app.credentials.set_credential import set_credential
#from set_credential import set_credential
# Get the list of datasets in the bigquery
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
    b = time()
    # Convert the result into a Pandas DataFrame
    c = time()
    df = query_job.to_dataframe()
    d = time()
    #df = pandas_gbq.read_gbq(query, credentials=set_credential(), dialect='standard', use_bqstorage_api=True)
    print(f"Time to read the data: {b-a}")
    print(f"Time to convert the data to dataframe: {d-c}")
    return df

def data_preprocessing(dataset):
    # eliminate all the CH (punctuation)
    dataset = dataset[dataset['tag_underthesea'] != 'CH']

    # sort the table by sequence
    dataset = dataset.sort_values(by='sequence')
    return dataset


def load_data(PROJECT_ID, DATASET_ID, TABLE_ID, size):
    credentials = set_credential()
    bigquery_client = bigquery.Client(credentials=credentials,
                                      project=PROJECT_ID)
    
    df = read_bq(PROJECT_ID, DATASET_ID, TABLE_ID, bigquery_client, size)
    df = data_preprocessing(df)

    return df

def data_description(df):
    # Get the head of the dataset
    dataset_head = df.head().to_dict(orient='records')
    data_html = df.to_html(index=False)
    data_html = data_html[data_html.find('\n'):data_html.rfind('\n')]
    # Convert dataset shape to dictionary
    dataset_shape = {"rows": df.shape[0], "columns": df.shape[1]}
    
    return data_html, dataset_shape

# df = load_data('intern-project-415606', 'Criminal_Dataset', 'criminal_data_inorder', 2000)
# print(data_description(df))