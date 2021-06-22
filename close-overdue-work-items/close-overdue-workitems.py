from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v6_0.work_item_tracking.models import Wiql
from azure.devops.v6_0.work_item_tracking.models import JsonPatchOperation
from wiutils import get_overdue_workitems
from wiutils import close_work_items

# Replace with your personal access token (PAT) and organization name
# Create PAT https://docs.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=preview-page#create-a-pat
personal_access_token = '<PAT>'
organization_url = 'https://dev.azure.com/<organization>'

credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get work items and close
wis = get_overdue_workitems(connection,2)
close_work_items(connection,wis)