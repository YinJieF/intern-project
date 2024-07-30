from google.cloud import storage
from app.credentials.set_credential import set_credential
def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # Initialize a storage client
    storage_client = storage.Client(credentials=set_credential())

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)

    # Get the blob (file) from the bucket
    blob = bucket.blob(source_blob_name)

    # Download the blob to the specified file
    blob.download_to_filename(destination_file_name)

    print(f"Downloaded storage object {source_blob_name} from bucket {bucket_name} to local file {destination_file_name}.")

# Replace these variables with your bucket name and file details
bucket_name = 'genai-project'
source_blob_name = 'prompt_text.txt'
destination_file_name = 'prompt_text.txt'

def get_prompt():
    download_blob(bucket_name, source_blob_name, destination_file_name)
    # read downloaded file
    with open(destination_file_name, 'r') as file:
        input_text = file.read()
        return input_text


