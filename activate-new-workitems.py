from lib.wiutils import activate_work_items, get_nonactivated_workitems
from config import *

connection = config.get_ado_connection()

# Get work items and activate
wis = get_nonactivated_workitems(connection,8)
activate_work_items(connection,wis)