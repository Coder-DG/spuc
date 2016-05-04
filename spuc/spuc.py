import click

import utils
from services import google


class Spuc(object):
    def __init__(self, credential_config_path, user_config_path):
        self.credential_config_dict = utils.convert_file_to_yaml(
                credential_config_path)
        self.user_config_dict = utils.convert_file_to_yaml(user_config_path)

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
