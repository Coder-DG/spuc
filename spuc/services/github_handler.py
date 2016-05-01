import requests

from spuc import utils


def invite_user(user_config, service_config):
    user_config = \
        utils.check_is_file_and_convert_from_yaml(user_config)['github']
    service_config = \
        utils.check_is_file_and_convert_from_yaml(service_config)['github']
    credentials = (service_config['username'], service_config['password'])

    response = requests.put(
            'https://api.github.com/orgs/'
            '{0}/memberships/{1}'.format(
                    user_config['organization'],
                    user_config['username']
            ),
            auth=credentials
    )

    return "Message: {0} | Status Code: {1}".format(
            response.text,
            response.status_code
    )
