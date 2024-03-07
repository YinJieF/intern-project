from google.cloud import billing
from google.oauth2 import service_account

# Path to the service account key file
service_account_key_file = 'intern-project-415606-df671484ed7a.json'

# Authenticate using service account credentials
credentials = service_account.Credentials.from_service_account_file(
    service_account_key_file)

# Initialize the CloudBillingClient
client = billing.CloudBillingClient(credentials=credentials)

# List all billing accounts
for account in client.list_billing_accounts():
    print(f"Billing Account ID: {account.name}")
    print(f"Display Name: {account.display_name}")
    print(f"Open: {account.open}")
    print()
