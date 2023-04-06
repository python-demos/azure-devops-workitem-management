from utils import emit
from azure.devops.v6_0.work_item_tracking.models import Wiql
from azure.devops.v6_0.work_item_tracking.models import JsonPatchOperation
import re
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
    emit("Updated {0} - ActualEndDate:{1} Field:{2},NewValue:{3}".format(wi.id,wi.fields["OpportunityPipeline.ActualEndDate"], idx,value))

#endregion

#region close
def close_work_item(connection,wi):
    emit(f"Closing workitem {wi.id}")
    update_work_item(connection,wi,'System.State','Closed')

def close_work_items(connection,wis):
    """Close work items"""
    list(map(lambda wi:close_work_item(connection,wi), wis))
#endregion

#region activate workitems

def activate_work_item(connection,wi):
    emit(f"Activate workitem {wi.id}")
    update_work_item(connection,wi,'System.State','Active')

def activate_work_items(connection,wis):
    """Activate work items"""
    list(map(lambda wi:activate_work_item(connection,wi), wis))

#endregion

#region get
def workitemids_to_workitems(wit_client,wiql_results):
    emit("{0} - Results: {1}".format(workitemids_to_workitems.__name__, len(wiql_results)))
    if wiql_results:
        # WIQL query gives a WorkItemReference with ID only, get the corresponding WorkItem from id using additional calls
        work_items = (
            wit_client.get_work_item(int(res.id)) for res in wiql_results
        )
        return work_items
    else:
        return []
def get_new_active_workitems(connection, limit=30):
    """Get new and active work items
    Args:
        connection : azure.devops.connection
            Connection to ADO
        limit : int, optional
            Number of items to fetch. Default to 30
    """
    wit_client = connection.clients.get_work_item_tracking_client()
    wiql = Wiql(
        query="""
        select [System.Id]
        from WorkItems
        where [System.WorkItemType] = 'Task'
            AND [System.State] <> 'Closed'
            AND [System.State] <> 'Removed'
            AND [System.AssignedTo] = @Me
        order by [System.ChangedDate] desc"""
    )
    wiql_results = wit_client.query_by_wiql(wiql, top=limit).work_items
    return workitemids_to_workitems(wit_client,wiql_results)

def get_overdue_workitems(connection,limit=30):
    """Get overdue work items (tasks only) based on OpportunityPipeline.ActualEndDate. Its a custom field. Replace with right value based on environment 
    Args:
        connection : azure.devops.connection
            Connection to ADO
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
            AND [OpportunityPipeline.ActualEndDate] < @Today
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

def get_nonactivated_workitems(connection,limit=30):
    """Get work items (tasks only) that are OpportunityPipeline.ActualStartDate > @Today> OpportunityPipeline.ActualEndDate. Its a custom field. Replace with right value based on environment 
    Args:
        connection : azure.devops.connection
            Connection to ADO
        limit : int, optional
            Number of items to fetch. Default to 30
    """
    wit_client = connection.clients.get_work_item_tracking_client()
    wiql = Wiql(
        query="""
        select [System.Id]
        from WorkItems
        where ([System.WorkItemType] = 'Task' OR [System.WorkItemType] = 'User Story')
            AND [System.State] = 'New'
            AND [System.AssignedTo] = @Me
            AND [OpportunityPipeline.ActualStartDate] <= @Today
            AND [OpportunityPipeline.ActualEndDate] >= @Today
        order by [System.ChangedDate] desc"""
    )
    wiql_results = wit_client.query_by_wiql(wiql, top=limit).work_items
    emit("Results: {0}".format(len(wiql_results)))
    return workitemids_to_workitems(wit_client,wiql_results)
#endregion