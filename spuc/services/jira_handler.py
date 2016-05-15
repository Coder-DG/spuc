from jira import JIRA

from spuc import utils


def create_user(user_config, service_config):
    user_config = \
        utils.convert_config_file(user_config)['jira']
    service_config = \
        utils.convert_config_file(service_config)['jira']

    jira = JIRA(options=service_config['jira_options'],
                basic_auth=(
                    service_config['username'],
                    service_config['password']
                ))
    return jira.add_user(**user_config)
