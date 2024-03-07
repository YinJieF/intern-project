from google.oauth2 import service_account
import googleapiclient.discovery

PROJECT_ID = 'intern-project-415606'
SA_FILE = 'intern-project-415606-df671484ed7a.json'
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

credentials = service_account.Credentials.from_service_account_file(
    filename=SA_FILE,
    scopes=SCOPES)

service = googleapiclient.discovery.build(
    'cloudresourcemanager', 'v3', credentials=credentials)

# Build a client for the Cloud IAM API
service_1 = googleapiclient.discovery.build(
    'iam', 'v1', credentials=credentials)

resource = 'projects/' + PROJECT_ID

response = service.projects().getIamPolicy(resource=resource, body={}).execute()

roles = []

for binding in response['bindings']:
    print('Role:', binding['role'])
    roles.append(binding['role'])
    
    for member in binding['members']:
        print(member, end=' | ')
    print('\n')
    

# Print the unique permissions
print(f"Total number of unique roles used in project {PROJECT_ID}: {len(response['bindings'])}\n")

for role in roles:
    if role == 'roles/owner' or role == 'roles/editor':
        print('Owner role [admin] is used in the project\n')
        continue
    role_details = service_1.roles().get(name=role).execute()
    permissions = role_details.get('includedPermissions', [])
    print(f"Role: {role}")
    print("Permissions:")
    for permission in permissions:
        print(f"- {permission}")
    print()
