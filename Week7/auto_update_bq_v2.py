# package required
# %pip install pandas-gbq
# %pip install underthesea

import pandas_gbq
from underthesea import ner
from google.cloud import bigquery

# read the (original) data from the bigquery
def read_bq(project_id, dataset_id, table_id):
  
    query = f"""
        SELECT * 
        FROM {project_id}.{dataset_id}.{table_id}
    """
  
    query_job = bigquery_client.query(query)

    # Convert the result into a Pandas DataFrame
    df = query_job.to_dataframe()

    return df
# check if table is created
def create_table(project_id, dataset_id, table_id_write):
    schema = [
        bigquery.SchemaField("extract_id", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("text", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("ner_underthesea", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("tag_underthesea", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("self_label", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("sequence", "INTEGER", mode="REQUIRED")
    ]
    table = bigquery.Table(f"{project_id}.{dataset_id}.{table_id_write}", schema=schema)
    try:
        table = bigquery_client.create_table(table)
        print(f"Table {project_id}.{dataset_id}.{table_id_write} created successfully.")
        return True
    except Exception as e:
        print(f"Table {project_id}.{dataset_id}.{table_id_write} already exists.")
        return False

# return the last row of data
def check_table(project_id, dataset_id, table_id_write):
    # Query to fetch the maximum extract_id and count of rows in the table
    query = f"""
            SELECT 
                MAX(extract_id) AS max_extract_id, 
                COUNT(*) AS total_rows
            FROM {project_id}.{dataset_id}.{table_id_write};
        """
    
    # Execute the query
    query_job = bigquery_client.query(query)

    # Fetch the result
    result = query_job.result()
    
    # Extract values from the result
    for row in result:
        return row['max_extract_id'], row['total_rows']

def ner_bq_update(project_id, dataset_id, df, table_id_write, set_index=0, sequence=0):
    for i in range(set_index, len(df)):
        ner_result = ner(df['EXTRACT'][i])

        rows = []
        for entity in ner_result:
            row = {
                "extract_id": i,  # You can use the index 'i' as the ID for each sentence
                "text": entity[0],
                "ner_underthesea": entity[3],
                "tag_underthesea": entity[1],
                "self_label": 'other',
                "sequence":sequence
            }
            sequence += 1
            # self label provided name as N
            if df['NAME'][i].strip() == row['text'].strip():
                row['self_label'] = 'N'
            # self label numeric data as M
            elif row['tag_underthesea'] == 'M' or row['text'].count('/') == 2:
                row['self_label'] = 'M'
            rows.append(row)
        
        errors = bigquery_client.insert_rows_json(f"{project_id}.{dataset_id}.{table_id_write}", rows)

        if i % 100 == 0:
            print(f"Inserted successfully for sentence {i}.")

if __name__ == "__main__":
    # Replace 'your-project-id' with your actual project ID
    PROJECT_ID = "intern-project-415606"
    # Dataset ID
    DATASET_ID = "Criminal_Dataset"
    # Table ID for reading the data
    TABLE_ID = "criminal_data"
    # Table ID for writing the data
    TABLE_ID_WRITE = "criminal_data_inorder"

    bigquery_client = bigquery.Client(project=PROJECT_ID)
    
    # Read the data from the BigQuery table
    df = read_bq(PROJECT_ID, DATASET_ID, TABLE_ID)
    
    if create_table(PROJECT_ID, DATASET_ID, TABLE_ID_WRITE):
        new_id, sequence = 0, 1
    else:
        new_id, sequence = check_table(PROJECT_ID, DATASET_ID, TABLE_ID_WRITE)
        new_id, sequence = int(new_id), int(sequence)
    # Update the data with named entity recognition, set start index (default = 0)
    ner_bq_update(PROJECT_ID, DATASET_ID, df, TABLE_ID_WRITE, new_id, sequence)