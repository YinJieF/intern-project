from google.cloud import bigquery
from set_credential import set_credential

def create_dataset(project_id, dataset_id):
    # Initialize a BigQuery client
    bigquery_client = bigquery.Client(credentials=set_credential())

    # Construct a dataset reference object
    dataset_ref = bigquery_client.dataset(dataset_id)

    # Construct a dataset object
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"  # Set the location where the dataset should be created (e.g., US)

    try:
        # Create the dataset
        bigquery_client.create_dataset(dataset, exists_ok=True)
        print(f"Dataset {project_id}.{dataset_id} created successfully.")
    except Exception as e:
        print(f"Failed to create dataset: {e}")

def create_table(project_id, dataset_id, table_id_write, bigquery_client):
    schema = [
        bigquery.SchemaField("QUESTION", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("ANSWER", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("USER_FEEDBACK", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("BQ_CREATED_DATE", "TIMESTAMP", mode="NULLABLE"),
        bigquery.SchemaField("BQ_UPDATED_DATE", "TIMESTAMP", mode="NULLABLE"),
    ]
    table = bigquery.Table(f"{project_id}.{dataset_id}.{table_id_write}", schema=schema)
    try:
        table = bigquery_client.create_table(table)
        return True
    except Exception as e:
        print(f"Table {project_id}.{dataset_id}.{table_id_write} already exists.")
        return False
    
bigquery_client = bigquery.Client(credentials=set_credential())
print(create_dataset("intern-project-415606", "llama_llm"))
print(create_table("intern-project-415606", "llama_llm", "llama_llm_result", bigquery_client))