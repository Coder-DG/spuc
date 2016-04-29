from jira import JIRA

from spuc import utils


def create_user(user_config, service_config):
    user_config = \
        utils.check_is_file_and_convert_from_yaml(user_config)['jira']
    service_config = \
        utils.check_is_file_and_convert_from_yaml(service_config)['jira']

    jira = JIRA(options=service_config['jira_options'],
                basic_auth=(
                    service_config['username'],
                    service_config['password']
                ))
    return jira.add_user(**user_config)
