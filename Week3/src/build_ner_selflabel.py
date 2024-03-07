#run on vertex ai workbench

import pandas as pd
from google.cloud import bigquery
from google.auth import credentials
from underthesea import ner

def load_dataset(project_id, dataset_id, table_id):
    # Load the original dataset from bigquery
    client = bigquery.Client()

    # Set the query
    query = """
        SELECT * 
        FROM `{project_id}.{dataset_id}.{table_id}`
    """

    # Run the query
    query_job = client.query(query)

    # Convert the results to a pandas DataFrame
    df = query_job.to_dataframe()

    return df

def bigquery_client():
    # Create a BigQuery client
    client = bigquery.Client()
    return client

def build_ner_table(project_id, client, dataset_id, new_table_id, schema):

    # Create a BigQuery table
    table = bigquery.Table(f"{project_id}.{dataset_id}.{new_table_id}", schema=schema)

    # Send the table creation request to the BigQuery API
    try:
        table = client.create_table(table)  # API request
        print(f"Table {new_table_id} created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")

def extract_ner(df, client, project_id, dataset_id, table_id):
    # carry out ner and insert into bigquery
    # set the scale of the data to insert
    for i in range(0, 1000):
        ner_result = ner(df['EXTRACT'][i])

        rows = []
        for entity in ner_result:
            row = {
                "extract_id": str(i),  # You can use the index 'i' as the ID for each sentence
                "text": entity[0],
                "ner_underthesea": entity[3],
                "tag_underthesea": entity[1],
                "self_label": 'other'
            }
            # self label provided name as N
            if df['NAME'][i].strip() == row['text'].strip():
                row['self_label'] = 'N'
            # self label numeric data as M
            elif row['tag_underthesea'] == 'M' or row['text'].count('/') == 2:
                row['self_label'] = 'M'
            rows.append(row)
            
        # for row in rows:
        #     print(row)
        # Insert each row into BigQuery
        errors = client.insert_rows_json(f"{project_id}.{dataset_id}.{table_id}", rows)

        if errors == []:
            print(f"Inserted successfully for sentence {i}.")
        else:
            print(f"Errors encountered while inserting rows for sentence {i}.")

if __name__ == "__main__":
    # Set up the environment
    project_id =  'intern-project-415606'
    dataset_id = 'Criminal_Dataset'
    table_id = 'criminal_data'

    # Load the dataset
    df = load_dataset(project_id, dataset_id, table_id)

    # Create a BigQuery client
    client = bigquery_client()

    # Define the schema for the new table
    schema = [
        bigquery.SchemaField("extract_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("text", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("ner_underthesea", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("tag_underthesea", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("self_label", "STRING", mode="REQUIRED")
    ]

    # Create the new table
    new_table_id = "criminal_data_ner"
    build_ner_table(project_id, dataset_id, new_table_id, schema)