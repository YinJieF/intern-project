#Create dataset in gbq
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

# Specify the dataset ID
dataset_id = 'Criminal_Dataset'

# Specify the table ID
table_id = 'criminal_data'

text = 'Trần Ngọc T'
def read_csv_file(text):
    df = pd.read_csv('Data_Criminal_GRAY_LIST.csv')
    for i in range(len(df)):
        if text in df['EXTRACT'][i]:
            return df['NAME'][i], df['BIRTH'][i]
            

def using_query(text):
    query = f"""
    SELECT COUNT(*)
    FROM `intern-project-415606.Criminal_Dataset.criminal_data`
    """
    # Execute the query
    query_job = client.query(query)

    # Fetch the results
    results = query_job.result()
    results = list(results)
    return results

print(read_csv_file(text))
print(using_query(text))