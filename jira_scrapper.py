import jira.client
import pandas as pd
from getpass import getpass
from jira.client import JIRA


class Inputs():
    get_jira_login = input(
        'Login: '
    )
    get_jira_password = getpass()

    get_jira_address = input(
        'Jira address: '
    )
    get_jira_project = input(
        'Project: '
    )
    get_jira_results = input(
        'Results to show: '
    )
    get_jira_excel = input(
        'Excel file name .xlsx: '
    )
    

if __name__=='__main__':

    jira_options={
        'server':Inputs.get_jira_address , 'verify':False
        }

    jira=JIRA(
        options=jira_options, basic_auth=(Inputs.get_jira_login, Inputs.get_jira_password)
        )

    issues_in_project = jira.search_issues(
        'project={0}'.format(Inputs.get_jira_project), startAt=0, maxResults=int(Inputs.get_jira_results)
        )

    issues = pd.DataFrame()

    for issue in issues_in_project:
        jira_data = {
            'key'               : issue.key,
            'assignee'          : issue.fields.assignee,
            'creator'           : issue.fields.creator,
            'reporter'          : issue.fields.reporter,
            'created'           : issue.fields.created,
            'components'        : issue.fields.components,
            'description'       : issue.fields.description,
            'summary'           : issue.fields.summary,
            'fixVersions'       : issue.fields.fixVersions,
            'subtask'           : issue.fields.issuetype.subtask,
            'issuetype'         : issue.fields.issuetype.name,
            'priority'          : issue.fields.priority.name,
            'resolution'        : issue.fields.resolution,
            'resolution.date'   : issue.fields.resolutiondate,
            'status.name'       : issue.fields.status.name,
            'status.description': issue.fields.status.description,
            'updated'           : issue.fields.updated,
            'versions'          : issue.fields.versions,
    }
        issues = issues.append(
            jira_data, ignore_index=True
            )

    issues.head()

    issues.to_excel(
        Inputs.get_jira_excel, sheet_name='1', encoding='UTF-8', index=False
        )
    
    