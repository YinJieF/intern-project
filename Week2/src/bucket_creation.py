from google.cloud import storage
from google.oauth2 import service_account

PROJECT_ID = 'intern-project-415606'
SA_FILE = 'intern-project-415606-df671484ed7a.json'
BUCKET_NAME = 'bucket-for-intern-project-415606'
#BUCKET_NAME = 'data-bucket-s09350704'

credentials = service_account.Credentials.from_service_account_file(SA_FILE)
# Create a storage client
storage_client = storage.Client(project=PROJECT_ID, credentials=credentials)

try:
    # Attempt to create the new bucket
    bucket = storage_client.create_bucket(BUCKET_NAME)
    print(f'Bucket {bucket.name} created.')
except Exception as e:
    # Handle other exceptions
    print(f'An error occurred: {e}')
