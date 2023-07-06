# Azure DevOps Workitems Management

Demos for managing Azure DevOps Work items.

> The demos are mostly done as part of automating my personal/company tasks. Those might not work as is in other environments.

# Running the code

- Clone
- Make sure the azure-devops is installed use the below command to install
  - `pip install azure-devops`
  - `pip install python-dateutil`
  - `pip install python-dotenv`
- Environment variables (Choose any one method)
  - Add [.env file](https://pypi.org/project/python-dotenv/)
    - Add `personal_access_token` and `organization_url` keys with respective values.
  - Set the environmet variable with the same above keys using the operatign system methods
- Run any of the below python files
    - `close-overdue-workitems.py`
    - `activate-new-workitems.py`
    - `sync-workitems.py` - change the Start and end dates of tasks to match the start and end dates on iteraction path

# Things to take care

- Min Python version - Tested using 3.8.5. There are no information about what is the miminum version required for [azure-devops](https://github.com/microsoft/azure-devops-python-api/) package that this code depends on.
- By default it closes only 2 work items. If you want to close more items change the number 2 in the below line of close-overdue-workitems.py file
  - `get_overdue_workitems(connection,2)`
- wiutils.py
  - The `get_overdue_workitems` function returns the workitems based on OpportunityPipeline.ActualEndDate. Its a custom field. Replace with right value based on environment.
  - It closes only work item types of Task. If you need to close other types modify the wiql query in `get_overdue_workitems` function. 
