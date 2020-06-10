from jira import JIRA

from spuc import utils


def create_user(user_config, service_config):
    service_config = utils.convert_config_file(service_config)
    user_configs = utils.convert_config_file(user_config)

    try:
        jira_service_config = service_config['jira']
        user_config = user_configs['jira']
    except KeyError as exception:
        raise exception

    jira = JIRA(options=jira_service_config['jira_options'],
                basic_auth=(
                    jira_service_config['username'],
                    jira_service_config['password']
                ))
    return jira.add_user(**user_config)
