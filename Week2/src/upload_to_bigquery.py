from google.cloud import bigquery
from google.oauth2 import service_account

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

# Create the dataset if it doesn't exist
dataset_ref = client.dataset(dataset_id)
dataset = bigquery.Dataset(dataset_ref)

try:
    dataset = client.create_dataset(dataset)  # API request
    print(f'Dataset {dataset.dataset_id} created.')
except Exception as e:
    print(f'Dataset {dataset.dataset_id} already exists.')

# Specify the table ID
table_id = 'criminal_data_gray_list'

# Path to your CSV file in Google Cloud Storage
source_uri = 'gs://bucket-for-intern-project-415606/Data_Criminal_GRAY_LIST.csv'

# Define the schema of your data (if it's not inferred)
# 'JLR_LINK', 'TRANS_TYPE_OF_CASE', 'TRANS_LEGAL_RELATIONSHIP', 'PDF_TEXT', 'EXTRACT', 'ID', 'NAME', 'Year', 'Month', 'Day', 'GENDER', 'BIRTH'
schema = [
    bigquery.SchemaField('JLR_LINK', 'STRING'),
    bigquery.SchemaField('TRANS_TYPE_OF_CASE', 'STRING'),
    bigquery.SchemaField('TRANS_LEGAL_RELATIONSHIP', 'STRING'),
    bigquery.SchemaField('PDF_TEXT', 'STRING'),
    bigquery.SchemaField('EXTRACT', 'STRING'),
    bigquery.SchemaField('ID', 'STRING'),
    bigquery.SchemaField('NAME', 'STRING'),
    bigquery.SchemaField('Year', 'INTEGER'),
    bigquery.SchemaField('Month', 'INTEGER'),
    bigquery.SchemaField('Day', 'INTEGER'),
    bigquery.SchemaField('GENDER', 'STRING'),
    bigquery.SchemaField('BIRTH', 'TIMESTAMP')
]

# Configure the job options
job_config = bigquery.LoadJobConfig(
    schema=schema,
    skip_leading_rows=1,  # if your CSV file has a header
    source_format=bigquery.SourceFormat.CSV,
)

# Start the job to load data from the CSV file into BigQuery
job = client.load_table_from_uri(
    source_uri,
    f'{project_id}.{dataset_id}.{table_id}',
    job_config=job_config,
)

# Wait for the job to complete
job.result()

print(f'Loaded {job.output_rows} rows into {dataset_id}.{table_id}')
