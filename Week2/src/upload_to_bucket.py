from google.cloud import storage
from google.oauth2 import service_account

# Path to the service account key file
service_account_key_file = 'intern-project-415606-df671484ed7a.json'

# Authenticate using service account credentials
credentials = service_account.Credentials.from_service_account_file(
    service_account_key_file)

# Set the name of the bucket and the path to the local file
BUCKET_NAME = 'bucket-for-intern-project-415606'
LOCAL_FILE_PATH = 'Data_Criminal_GRAY_LIST.csv'
DESTINATION_FILE_NAME = 'Data_Criminal_GRAY_LIST.csv'
# LOCAL_FILE_PATH = 'customers-1000.csv'
# DESTINATION_FILE_NAME = 'customers-1000.csv'

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    try:
        blob.upload_from_filename(source_file_name)
    except Exception as e:
        print(f'An error occurred: {e}')
        return
      
    print(f'File {source_file_name} uploaded to {bucket_name} as {destination_blob_name}.')

# Call the function to upload the file
upload_blob(BUCKET_NAME, LOCAL_FILE_PATH, DESTINATION_FILE_NAME)
