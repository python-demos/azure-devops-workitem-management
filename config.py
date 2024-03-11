from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from dotenv.main import load_dotenv
import os
class config:
    # Create PAT https://docs.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=preview-page#create-a-pat
    def get_ado_connection():
        load_dotenv()
        personal_access_token = os.environ['personal_access_token']
        organization_url = os.environ['organization_url']
        credentials = BasicAuthentication('', personal_access_token)
        connection = Connection(base_url=organization_url, creds=credentials)    
        return connection