from config import *

from azure.devops.v7_1.work_item_tracking.models import Wiql,TeamContext
#region iterations
def list_iterations_for_all_teams(connection, project_name):
    """
    List iteration paths for all teams in a given Azure DevOps project.

    Args:
        connection: The Azure DevOps connection object.
        project_name: The name of the Azure DevOps project.

    Returns:
        A dictionary where keys are team names and values are lists of iteration paths.
    """
    # Get the core client to fetch teams
    core_client = connection.clients.get_core_client()
    teams = core_client.get_teams(project_id=project_name)
    work_client = connection.clients.get_work_client()
    team_iterations = {}

    for team in teams:
        team_name = team.name
        team_context = TeamContext(project=project_name, team=team_name)
        iterations = work_client.get_team_iterations(team_context)
        iteration_paths = [iteration.path for iteration in iterations]
        team_iterations[team_name] = iteration_paths
        print(f"Team: {team_name}")
        for iteration in iterations:
            print(f"  Iteration Path: {iteration.path}")
            print(f"    Start Date: {iteration.attributes.start_date}")
            print(f"    End Date: {iteration.attributes.finish_date}")

    return team_iterations
def get_all_iterations_project(connection,project_name):
    """Get iterations for a project
    Args:
        work_client : azure.devops.v7_1.work_item_tracking.work_item_tracking_client.WorkItemTrackingClient
            Work item tracking client
        project_name : str
            Project name
    """
    wit_client = connection.clients.get_work_client()
    #wit_client.get_team
    iterations = wit_client.get_project_iterations(project_name)
    # # Find the iteration matching the given path
    for iteration in iterations:
        emit("{0}: {1}: {2} : {3} - {4}".format(iteration.name,iteration.id,iteration.path, iteration.attributes.start_date,iteration.attributes.finish_date))
    # if iteration.name == iteration_name:
    #             # Return the start and end dates
    #     return iteration.attributes.start_date, iteration.attributes.finish_date
    # return None, None
    return iterations
def get_iterations(connection,project_name,team_name):
    """Get iterations for a team
    Args:
        work_client : azure.devops.v7_1.work_item_tracking.work_item_tracking_client.WorkItemTrackingClient
            Work item tracking client
        project_name : str
            Project name
        team_name : str
            Team name
    """
    wit_client = connection.clients.get_work_client()
    team = TeamContext(project= project_name , team = team_name,team_id=None) 
    iterations = wit_client.get_team_iterations(team)
    # # Find the iteration matching the given path
    for iteration in iterations:
        emit("{0}: {1}: {2} : {3} - {4}".format(iteration.name,iteration.id,iteration.path, iteration.attributes.start_date,iteration.attributes.finish_date))
    # if iteration.name == iteration_name:
    #             # Return the start and end dates
    #     return iteration.attributes.start_date, iteration.attributes.finish_date
    # return None, None
    return iterations