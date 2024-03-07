from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to the service account key file
service_account_key_file = 'intern-project-415606-df671484ed7a.json'

# Authenticate using service account credentials
credentials = service_account.Credentials.from_service_account_file(
    service_account_key_file)

# Build a client for the Cloud Resource Manager API
service = build('cloudresourcemanager', 'v1', credentials=credentials)

# Retrieve information about the project
project_info = service.projects().get(projectId='intern-project-415606').execute()

# Print project information
print("Project Information:")
print("Project ID:", project_info['projectId'])
print("Project Name:", project_info['name'])
print("Project Number:", project_info['projectNumber'])
