# Does the below actions
# 1. Change the start and end dates to match with the dates in iteration path if iteration path has date.
from config import *
from lib.wiutils import get_new_active_workitems,update_work_item
from lib.wcutils import get_iterations, get_all_iterations_project,list_iterations_for_all_teams
import re
from dateutil import parser

def get_start_end_dates(iteractionPath):
    """Get start and end dates from iteraction path. This works only if the iteraction path has dates in specific format of dd-MMM-yy or dd-MMM-yyyy. 
    If the date is not in this format, it will return None
    """
    dates = re.findall(r'[0-9]+-\w{3}-\d{4}',iteractionPath)
    if(len(dates)==0):
        dates = re.findall(r'[0-9]+-\w{3}-\d{2}',iteractionPath)
    iteractionStartDateStr= dates[0] if len(dates) == 2 else None
    iteractionStartDate = parser.parse(iteractionStartDateStr) if iteractionStartDateStr !=None else None
    iteractionEndDateStr= dates[1] if len(dates)==2 else None
    iteractionEndDate = parser.parse(iteractionEndDateStr) if iteractionEndDateStr != None else None
    return iteractionStartDate, iteractionEndDate

def update_date_ifnot_same(connection,wi,dateField,correctDate):
    if dateField in wi.fields.keys():
        existingDateStr = wi.fields[dateField]
        existingDate = parser.parse(existingDateStr)
    if 'existingDate' not in locals():
        print("{3} : workitem {0} - existingdate{1} is empty. givendate{2}. Updating...".format(__name__,wi.id,dateField,correctDate,update_date_ifnot_same.__name__))
        update_work_item(connection,wi,dateField,correctDate)
    elif existingDate.date() == correctDate.date():
        print("{0} : workitem {1} - existingdate[{2}] = {3} is same as givendate {4}".format(update_date_ifnot_same.__name__,wi.id,dateField, existingDate,correctDate))
    else:
        print("{5} : workitem {0} - existingdate[{1}] ={2} not same as givendate{3}. Updating...".format(__name__,wi.id,dateField,existingDate,correctDate,update_date_ifnot_same.__name__))
        update_work_item(connection,wi,dateField,correctDate)

def update_dates_if_outofsync(connection,wi):
    iteractionPath =  wi.fields["System.IterationPath"]
    iteractionStartDate, iteractionEndDate = get_start_end_dates(iteractionPath)
    #TODO handle situations where the iteraction path is not available.
    if iteractionStartDate != None:
        update_date_ifnot_same(connection,wi,"OpportunityPipeline.ActualStartDate",iteractionStartDate)
    if iteractionEndDate !=None:
        update_date_ifnot_same(connection,wi,"OpportunityPipeline.ActualEndDate",iteractionEndDate)

connection = config.get_ado_connection()
wis=get_new_active_workitems(connection,20)
#list_iterations_for_all_teams(connection=connection, project_name="KPMG-Clara")
#get_all_iterations_project(connection=connection,project_name="KPMG-Clara")
#get_iterations(connection, team_name=None, project_name="KPMG-Clara")
list(map(lambda wi:update_dates_if_outofsync(connection,wi), wis))
