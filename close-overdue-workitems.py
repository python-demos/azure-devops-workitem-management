from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v6_0.work_item_tracking.models import Wiql
from azure.devops.v6_0.work_item_tracking.models import JsonPatchOperation
from lib.wiutils import get_overdue_workitems,close_work_items, print_work_items
from config import *

# Replace with your personal access token (PAT) and organization name
# Create PAT https://docs.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=preview-page#create-a-pat
credentials = BasicAuthentication('', config.personal_access_token)
connection = Connection(base_url=config.organization_url, creds=credentials)

# Get work items and close
wis = get_overdue_workitems(connection,8)
#print_work_items(wis)
close_work_items(connection,wis)
