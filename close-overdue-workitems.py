from lib.wiutils import get_overdue_workitems,close_work_items
from config import *

connection = config.get_ado_connection()

# Get work items and close
wis = get_overdue_workitems(connection,8)
close_work_items(connection,wis)
