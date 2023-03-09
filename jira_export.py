# Description: This script will iterate through all issues in a Jira project and return the following information:

# Import the necessary libraries
import json
from jira.client import JIRA

"""
This script will iterate through all issues in a Jira project and return the following information:
- Summary
- Status
- Assignee
- Reporter
- Priority
- Created
- Updated
- Description
- Labels
- Components
- FixVersions
- AffectsVersions
- IssueType
- Worklogs
- Comments

The script will also return the total time spent on the issue.

The script will return the data in a JSON file.
        
"""
# workspace is the name of your Jira workspace. For example, if your Jira URL is https://your-workspace.atlassian.net, then your workspace is your-workspace.
# email is your Jira username
# password is your jira Token that is generated from https://id.atlassian.com/manage-profile/security/api-tokens
# project is the project key for the Jira project you want to iterate through. For example, if your Jira URL is https://your-workspace.atlassian.net/browse/ABC-123, then your project key is ABC.
options = {'server': 'https://your-workspace.atlassian.net'}
jira = JIRA(options, basic_auth=("email", "password"))

size = 1000  # set the page size
initial = 0
issues_list = []  # create an empty list to hold the issues

while True:
    start = initial*size
    # project code is the project key for the Jira project you want to iterate through. For example, if your Jira URL is https://your-workspace.atlassian.net/browse/ABC-123, then your project key is ABC.
    issues = jira.search_issues('project=project-code',  start, size)
    if len(issues) == 0:
        break
    initial += 1
    for issue in issues:
        # check if worklogs exist for the issue
        if issue.fields.worklog.worklogs:
            # get the total time spent on the issue
            total_time_spent = sum([int(worklog.timeSpentSeconds)
                                   for worklog in issue.fields.worklog.worklogs])
            # create a list of worklogs containing the author, time spent, and comment
            worklogs = [{'Author': str(worklog.author),
                         'TimeSpentSeconds': str(worklog.timeSpentSeconds)} for worklog in issue.fields.worklog.worklogs]
            comments = [{'Author': str(comment.author),
                         'Comment': str(comment.body)} for comment in issue.fields.comment.comments]

        else:
            total_time_spent = None  # set total time spent to None if worklogs do not exist
            worklogs = None  # set worklogs to None if worklogs do not exist

        # create a dictionary with the relevant issue fields and worklog data
        issue_dict = {
            'project': 'NP',
            'Summary': issue.fields.summary,
            'Status': str(issue.fields.status),
            'Assignee': str(issue.fields.assignee),
            'Reporter': str(issue.fields.reporter),
            'Priority': str(issue.fields.priority),
            'Created': str(issue.fields.created),
            'Updated': str(issue.fields.updated),
            'Description': str(issue.fields.description),
            'Labels': [str(label) for label in issue.fields.labels],
            'Components': [str(comp) for comp in issue.fields.components],
            'FixVersions': [str(fix) for fix in issue.fields.fixVersions],
            'AffectsVersions': [str(ver) for ver in issue.fields.versions],
            'IssueType': str(issue.fields.issuetype),
            'TotalTimeSpentSeconds': total_time_spent,
            'Worklogs': worklogs,
            'Comments': comments,
            'Key': issue.key,
            'URL': f"https://beyonderissolutions.atlassian.net/browse/{issue.key}"
        }
        issues_list.append(issue_dict)  # add the issue dictionary to the list

# write the issues list to a JSON file
with open('issues.json', 'w') as f:
    json.dump(issues_list, f, indent=4)
