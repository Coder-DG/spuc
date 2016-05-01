import httplib2
from googleapiclient import discovery

from spuc import utils


def create_user(user_config, service_config):
    user_config = \
        utils.check_is_file_and_convert_from_yaml(user_config)['gapps']
    service_config = \
        utils.check_is_file_and_convert_from_yaml(service_config)['gapps']

    credentials = utils.get_oauth_credentials(
            credential_config_dict=service_config,
            scopes=utils.GOOGLE_SCOPES,
            name_prefix='google'
    )

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('admin', 'directory_v1', http=http)

    result = service.users().insert(body=user_config).execute()
    return result
