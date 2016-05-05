import click

import utils
from services import google


class Spuc(object):
    def __init__(self, config_path, user_config_path):
        self.config_dict = utils.convert_file_to_yaml(
                config_path)
        self.user_config_dict = utils.convert_file_to_yaml(user_config_path)

    def create_all(self):
        credentials = utils.get_oauth_credentials(
                credential_config_dict=self.config_dict['gapps'],
                scopes=utils.GOOGLE_SCOPES,
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
    google.create_user(
            utils.convert_file_to_yaml(user_yaml_path)['gapps'],
            utils.get_oauth_credentials(
                    utils.convert_file_to_yamlcredential_config_path)[
                'gapps'],
            utils.GOOGLE_SCOPES,
            'google'
    )
