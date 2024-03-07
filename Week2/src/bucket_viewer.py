from google.cloud import storage
from google.oauth2 import service_account

# Path to the service account key file
service_account_key_file = 'intern-project-415606-df671484ed7a.json'

# Authenticate using service account credentials
credentials = service_account.Credentials.from_service_account_file(
    service_account_key_file)

def list_buckets():
    """Lists all buckets."""
    storage_client = storage.Client(credentials=credentials)
    buckets = list(storage_client.list_buckets())

    print('Buckets:')
    for bucket in buckets:
        print(bucket.name)
        blobs = list(storage_client.list_blobs(bucket))
        for blob in blobs:
            print(blob.name)

# Call the function to list buckets
list_buckets()
