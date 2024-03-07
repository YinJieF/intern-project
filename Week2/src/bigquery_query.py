from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd

# Path to the service account key file
service_account_key_file = 'intern-project-415606-df671484ed7a.json'

# Authenticate using service account credentials
credentials = service_account.Credentials.from_service_account_file(
    service_account_key_file)

# Initialize a BigQuery client
client = bigquery.Client(credentials=credentials)

# Specify your Google Cloud Platform project ID
project_id = 'intern-project-415606'
dataset_id = 'customer_data'
table_id = 'customer_data_table'
table_id = 'Walmart_sales_table'
#run a sql query to get the data from the table
query = f"""
    SELECT *
    FROM `{project_id}.{dataset_id}.{table_id}`
    LIMIT 5
"""

query_job = client.query(query)
results = query_job.result()
for row in results:
    print(row)
    