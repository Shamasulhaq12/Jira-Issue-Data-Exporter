# Jira Issue Data Exporter

This script allows you to export all issues in a Jira project and their associated data to a JSON file. The following information is included for each issue:

    -Summary
    -Status
    -Assignee
    -Reporter
    -Priority
    -Created
    -Updated
    -Description
    -Labels
    -Components
    -FixVersions
    -AffectsVersions
    -IssueType
    -Worklogs
    -Comments
    -Total time spent

#### Prerequisites

    -Python 3
    -jira library (can be installed via pip)
    -Jira account with access to the project you want to export data from
    -Jira API token (can be generated from here)

#### Usage

1- Clone the repository and navigate to the directory.
2-Install the jira library by running the following command in the terminal:

    `pip install jira`
3- Open the jira_export.py file in a text editor and replace the following values with your own:
- your-workspace: the name of your Jira workspace (e.g. if your Jira URL is <https://your-workspace.atlassian.net>, then your workspace is your-workspace)
    - email: your Jira username
    - password: your Jira API token
    - project-code: the project key for the Jira project you want to export data from (e.g. if your Jira URL is <https://your-workspace.atlassian.net/browse/ABC-123>, then your project key is ABC)
  
4- Save the jira_export.py file.
5- Run the script by executing the following command in the terminal:

    `python jira_export.py`
6- The script will output a issues.json file in the same directory as the script. This file will contain all issues and their associated data in JSON format.

#### Notes

The script will export all issues in the project, regardless of their status.
The script uses Jira API pagination to iterate through all issues. The default page size is 1000, but you can change this by modifying the size variable in the script.
If a field is empty for an issue, it will be represented as None in the JSON output.
