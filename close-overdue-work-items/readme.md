# Running the code
- Clone
- Make sure the azure-devops is installed use the below command to install
  - `pip install azure-devops`
- close-overdue-workitems.py
  - Replace the <PAT> token
  - Replace the <organization> token
- Run the close-overdue-workitems.py file.

# Things to take care

- Min Python version - Tested using 3.8.5. There are no information about what is the miminum version required for [azure-devops](https://github.com/microsoft/azure-devops-python-api/) package that this code depends on.
- By default it closes only 2 work items. If you want to close more items change the number 2 in the below line of close-overdue-workitems.py file
  - `get_overdue_workitems(connection,2)`
- wiutils.py
  - The `get_overdue_workitems` function returns the workitems based on OpportunityPipeline.ActualEndDate. Its a custom field. Replace with right value based on environment.
  - It closes only work item types of Task. If you need to close other types modify the wiql query in `get_overdue_workitems` function. 
