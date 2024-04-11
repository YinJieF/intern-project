from google.oauth2 import service_account
def set_credential():
    # Path to the service account key file
    service_account_key_file = 'credential/intern-project-415606-52697549f6e1.json'
    # Authenticate using service account credentials
    credentials = service_account.Credentials.from_service_account_file(service_account_key_file)
    return credentials