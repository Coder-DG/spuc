import yaml
import os

import click
from oauth2client import client
from oauth2client import file
from oauth2client import tools

from services import google

GOOGLE_SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'
APPLICATION_NAME = 'SPUC'


class User:
    def __init__(self, credential_config_path=None):
        self.credential_config = self.convert_file_to_yaml(
                credential_config_path)


    def get_credentials(self, credential_config_path, scopes, name_prefix):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(
                credential_dir,
                '{0}_credentials.json'.format(name_prefix)
        )

        store = file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(
                    credential_config_path,
                    scopes
            )
            flow.user_agent = APPLICATION_NAME
            flags = tools.argparser.parse_args(args=[])
            credentials = tools.run_flow(flow, store, flags)
            print('Storing credentials to ' + credential_path)
        return credentials

    def create_in_google(self, user_yaml_path):
        credentials = self.get_credentials(
                credential_config_path=self.credential_config,
                scopes=GOOGLE_SCOPES,
                name_prefix='google'
        )

        print google.create_user(
                self.convert_file_to_yaml(user_yaml_path),
                credentials
        )

    def create_in_aws(self):
        pass

    def create_in_github(self):
        pass

    def create_in_jira(self):
        pass

    def convert_file_to_yaml(self, yaml_file_path):
        with open(str(yaml_file_path)) as yaml_file:
            return yaml.load(yaml_file)


@click.group()
def main():
    pass


@main.group()
def googleapps():
    pass


@googleapps.command(name='create')
@click.option('-c', '--credential-config-path',
              help='The path to user credential file.',
              required=True)
@click.option('-j', '--user-yaml-path',
              help='The path to the user yaml file.'
                   ' In this case, a Google user configuration.',
              required=True)
def create_user_google(credential_config_path, user_yaml_path):
    user_google = User(
            credential_config_path=credential_config_path
    )

    user_google.create_in_google(user_yaml_path)
