from google.oauth2 import service_account

def set_credential():
    # Path to the service account key file
    service_account_key_file = "./app/credentials/intern-project-415606-af2c42eb5ad4.json"
    # Authenticate using service account credentials
    credentials = service_account.Credentials.from_service_account_file(service_account_key_file)
    return credentials