from utils import emit
from azure.devops.v6_0.work_item_tracking.models import Wiql
from azure.devops.v6_0.work_item_tracking.models import JsonPatchOperation

#region print to console

def print_work_items(work_items):
    list(map(print_work_item,work_items))

def print_work_item(work_item):
    emit(
        "{0} {1}: {2} : {3} - {4}".format(
            work_item.fields["System.WorkItemType"],
            work_item.id,
            work_item.fields["OpportunityPipeline.ActualEndDate"],
            work_item.fields["System.State"],
            work_item.fields["System.Title"],
        )
    )
#endregion

#region update
def update_work_item(connection,wi,idx,value):
    patch_document = [
                    JsonPatchOperation(
                        op="replace",
                        path=f"/fields/{idx}",
                        value=value,
                    )
                ]
    wit_client = connection.clients.get_work_item_tracking_client()
    wit_client.update_work_item(patch_document,wi.id)
    emit("Updated {0} - Field:{1},NewValue:{2}".format(wi.id,idx,value))

#endregion

#region close
def close_work_item(connection,wi):
    update_work_item(connection,wi,'System.State','Closed')

def close_work_items(connection,wis):
    """Close work items"""
    list(map(lambda wi:close_work_item(connection,wi), wis))
#endregion

#region get
def get_overdue_workitems(connection,limit=30):
    """Get overdue work items (tasks only) based on OpportunityPipeline.ActualEndDate. Its a custom field. Replace with right value based on environment 
    Args:
        connection : azure.devops.connection
            The sound the animal makes (default is None)
        limit : int, optional
            Number of items to fetch. Default to 30
    """
    wit_client = connection.clients.get_work_item_tracking_client()
    wiql = Wiql(
        query="""
        select [System.Id],
            [System.WorkItemType],
            [System.Title],
            [System.State],
            [System.AreaPath],
            [System.IterationPath],
            [OpportunityPipeline.ActualEndDate]
        from WorkItems
        where [System.WorkItemType] = 'Task'
            AND [System.State] <> 'Closed'
            AND [System.State] <> 'Removed'
            AND [System.AssignedTo] = @Me
            AND [OpportunityPipeline.ActualEndDate] <= @Today
        order by [System.ChangedDate] desc"""
    )
    wiql_results = wit_client.query_by_wiql(wiql, top=limit).work_items
    emit("Results: {0}".format(len(wiql_results)))
    if wiql_results:
        # WIQL query gives a WorkItemReference with ID only
        # => we get the corresponding WorkItem from id using additional calls
        work_items = (
            wit_client.get_work_item(int(res.id)) for res in wiql_results
        )
        return work_items
    else:
        return []
#endregion
