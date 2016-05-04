import click

import utils
from services import google

GOOGLE_SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'


class Spuc(object):
    def __init__(self, credential_config_path, user_config_path):
        self.credential_config_dict = self.convert_file_to_yaml(
                credential_config_path)
        self.user_config_dict = self.convert_file_to_yaml(user_config_path)

    def convert_file_to_yaml(self, yaml_file_path):
        with open(str(yaml_file_path)) as yaml_file:
            return yaml.load(yaml_file)

    def create_all(self):
        credentials = utils.get_oauth_credentials(
                credential_config_dict=self.credential_config_dict['gapps'],
                scopes=GOOGLE_SCOPES,
                name_prefix='google'
        )

        print google.create_user(self.user_config_dict['gapps'],
                                 credentials
                                 )


@click.group()
def main():
    pass


@main.group()
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
    user_google = Spuc(
            credential_config_path,
            user_yaml_path
    )

    user_google.create_in_google()
