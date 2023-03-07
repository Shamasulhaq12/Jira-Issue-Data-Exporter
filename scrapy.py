
# from jira.client import JIRA
# options = {'server': 'https://beyonderissolutions.atlassian.net'}
# jira = JIRA(options, basic_auth=('shamsulhaq@beyonderissolutions.com',
#             'ATATT3xFfGF0FaWprW6Xu7eq6nbLqJ61dgs5qMS2VnauyTjcQ6K8Mx6aDm370kARhTYh3oPCE2R1ShEhnZKlG1yQhB3GyCsfrwsWzm7lphJRxv0f8tKkjuUECjEiID2yPkePzPOvx3ir-W5vnzXoUoVoIq5vC61in4Te2SZI3fj7YnadD5w5DfY=10B5049E'))


# size = 100
# initial = 0
# while True:
#     start = initial*size
#     issues = jira.search_issues('project=NP',  start, size)
#     if len(issues) == 0:
#         break
#     initial += 1
#     for issue in issues:
#         print('Summary=', issue.fields.summary)
#         print('Status=', issue.fields.status)
#         print('Assignee=', issue.fields.assignee)
#         print('Reporter=', issue.fields.reporter)
#         print('Priority=', issue.fields.priority)
#         print('Created=', issue.fields.created)
#         print('Updated=', issue.fields.updated)
#         print('Description=', issue.fields.description)
#         print('Labels=', issue.fields.labels)
#         print('Components=', issue.fields.components)
#         print('FixVersions=', issue.fields.fixVersions)
#         print('AffectsVersions=', issue.fields.versions)
#         print('IssueType=', issue.fields.issuetype)

# for i in jira.search_issues('filter=144', maxResults=15):
#     print(i.fields.summary)

# import scrapy


# class JiraSpider(scrapy.Spider):
#     name = 'jira_spider'
#     start_urls = ['https://beyonderissolutions.atlassian.net/login.jsp']

#     def parse(self, response):
#         return scrapy.FormRequest.from_response(
#             response,
#             formdata={'username': 'shamsulhaq@beyonderissolutions.com',
#                       'password': 'ATATT3xFfGF0FaWprW6Xu7eq6nbLqJ61dgs5qMS2VnauyTjcQ6K8Mx6aDm370kARhTYh3oPCE2R1ShEhnZKlG1yQhB3GyCsfrwsWzm7lphJRxv0f8tKkjuUECjEiID2yPkePzPOvx3ir-W5vnzXoUoVoIq5vC61in4Te2SZI3fj7YnadD5w5DfY=10B5049E'},
#             callback=self.after_login
#         )

#     def after_login(self, response):
#         # Check if login was successful by inspecting the response
#         if "authentication failed" in response.text:
#             self.logger.error("Login failed")
#             return
#         else:
#             pass
#             # Continue with your scraping logic
#             # ...


import json
from jira.client import JIRA

options = {'server': 'https://beyonderissolutions.atlassian.net'}
jira = JIRA(options, basic_auth=('shamsulhaq@beyonderissolutions.com',
            'ATATT3xFfGF0FaWprW6Xu7eq6nbLqJ61dgs5qMS2VnauyTjcQ6K8Mx6aDm370kARhTYh3oPCE2R1ShEhnZKlG1yQhB3GyCsfrwsWzm7lphJRxv0f8tKkjuUECjEiID2yPkePzPOvx3ir-W5vnzXoUoVoIq5vC61in4Te2SZI3fj7YnadD5w5DfY=10B5049E'))

size = 100
initial = 0
issues_list = []  # create an empty list to hold the issues
while True:
    start = initial*size
    issues = jira.search_issues('project=NP',  start, size)
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
