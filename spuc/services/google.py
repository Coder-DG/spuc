import click

import httplib2
from googleapiclient import discovery

from spuc import utils


def create_user(user_yaml, credentials):
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('admin', 'directory_v1', http=http)

    result = service.users().insert(body=user_yaml).execute()
    return result


@click.group()
def gapps():
    pass


@gapps.command(name='create')
@click.option('-c', '--credential-config-path',
              help='The path to admin credential file.',
              required=True)
@click.option('-u', '--user-yaml-path',
              help='The path to the user yaml config file.',
              required=True)
def create_user_google(credential_config_path, user_yaml_path):
    create_user(
            utils.convert_file_to_yaml(user_yaml_path)['gapps'],
            utils.get_oauth_credentials(
                    utils.convert_file_to_yamlcredential_config_path)[
                'gapps'],
            utils.GOOGLE_SCOPES,
            'google'
    )
