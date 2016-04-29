from jira import JIRA


def create_user(new_user_dict, username, password):
    jira_options = {'server': 'https://remove-this-url.atlassian.net/'}

    jira = JIRA(options=jira_options,
                basic_auth=(username, password))
    return jira.add_user(**new_user_dict)
