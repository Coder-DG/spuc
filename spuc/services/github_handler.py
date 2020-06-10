import requests

from spuc import utils


def invite_user(user_config, service_config):
    if not user_config:
        raise utils.SpucException('No user config was provided')
    if not service_config:
        raise utils.SpucException('No service config was provided')

    service_config = utils.convert_config_file(service_config)
    user_configs = utils.convert_config_file(user_config)

    try:
        github_service_config = service_config['github']
        user_config = user_configs['github']
        credentials = (
            github_service_config['username'],
            github_service_config['password']
        )
        user_organization = user_config['organization']
        username = user_config['username']
    except KeyError as exception:
        raise exception

    response = requests.put(
            'https://api.github.com/orgs/'
            '{0}/memberships/{1}'.format(
                    user_organization,
                    username
            ),
            auth=credentials
    )

    status_code = response.status_code
    if 300 > status_code >= 200 and response.text:
        return "Message: {0} | Status Code: {1}".format(
                response.text,
                response.status_code
        )

    raise RuntimeError(
            'GitHub server responded with status {0}'
            ' and the message: {1}'.format(
                    status_code,
                    response.text
            )
    )
