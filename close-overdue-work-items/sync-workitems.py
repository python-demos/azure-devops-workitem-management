# Does the below actions
# 1. Change the start and end dates to match with the dates in iteration path if iteraction path has date.
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from config import *
from wiutils import get_new_active_workitems,update_work_item
import re
from dateutil import parser
credentials = BasicAuthentication('', config.personal_access_token)
connection = Connection(base_url=config.organization_url, creds=credentials)

def get_start_end_dates(iteractionPath):
    """Get start and end dates from iteraction path. This works only if the iteraction path has dates in specific format of dd-MMM-yy
    """
    dates = re.findall(r'\d{2}-\w{3}-\d{2}',iteractionPath)
    iteractionStartDateStr= dates[0]
    iteractionStartDate = parser.parse(iteractionStartDateStr)
    iteractionEndDateStr= dates[1]
    iteractionEndDate = parser.parse(iteractionEndDateStr)
    return iteractionStartDate, iteractionEndDate

def update_date_ifnot_same(connection,wi,dateField,correctDate):
    existingDateStr = wi.fields[dateField]
    existingDate = parser.parse(existingDateStr)
    if existingDate.date() == correctDate.date():
        print("workitem {0} - existingdate[{1}] = {2} is same as givendate {3} ".format(wi.id,dateField, existingDate,correctDate))
    else:
        print("workitem {0} - existingdate[{1}] ={2} not same as givendate{3}. Updating...".format(wi.id,dateField,existingDate,correctDate))
        update_work_item(connection,wi,dateField,correctDate)

def update_dates_if_outofsync(connection,wi):
    iteractionPath =  wi.fields["System.IterationPath"]
    iteractionStartDate, iteractionEndDate = get_start_end_dates(iteractionPath)
    #TODO handle situations where the iteraction path is not available.
    update_date_ifnot_same(connection,wi,"OpportunityPipeline.ActualStartDate",iteractionStartDate)
    update_date_ifnot_same(connection,wi,"OpportunityPipeline.ActualEndDate",iteractionEndDate)

wis=get_new_active_workitems(connection,10)
list(map(lambda wi:update_dates_if_outofsync(connection,wi), wis))