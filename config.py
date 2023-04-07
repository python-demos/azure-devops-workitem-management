from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

class config:
    # Create PAT https://docs.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=preview-page#create-a-pat
    personal_access_token = '<YOUR PAT>'
    organization_url = 'https://dev.azure.com/<YOUR ORGANIZATION>'
    def get_ado_connection():
        credentials = BasicAuthentication('', config.personal_access_token)
        connection = Connection(base_url=config.organization_url, creds=credentials)    
        return connection