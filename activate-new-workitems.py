from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from lib.wiutils import activate_work_items, get_nonactivated_workitems
from config import *
# Replace with your personal access token (PAT) and organization name
# Create PAT https://docs.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=preview-page#create-a-pat

credentials = BasicAuthentication('', config.personal_access_token)
connection = Connection(base_url=config.organization_url, creds=credentials)

# Get work items and close
wis = get_nonactivated_workitems(connection,8)
activate_work_items(connection,wis)