from jira import JIRA


def create_user(user_json, credentials, jira_options):
    jira = JIRA(options=jira_options['jira_options'],
                basic_auth=(
                    credentials['credentials']['username'],
                    credentials['credentials']['password']
                ))
    return jira.add_user(**user_json['jira_user'])
