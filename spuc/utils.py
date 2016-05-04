import os
import json
import yaml
import tempfile

from oauth2client import client
from oauth2client import file
from oauth2client import tools

APPLICATION_NAME = 'SPUC'
GOOGLE_SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'


def get_oauth_credentials(credential_config_dict, scopes, name_prefix):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    oauth_credential_path = create_credential_json(
            credential_config_dict)
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
                oauth_credential_path,
                scopes
        )
        flow.user_agent = APPLICATION_NAME
        flags = tools.argparser.parse_args(args=[])
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials


def create_credential_json(credential_dict):
    tmp_dir_path = tempfile.mkdtemp()
    file_path = tmp_dir_path + 'spuc_secret.json'
    with open(file_path, 'w') as output:
        json.dump(credential_dict, output)
    return file_path


def convert_file_to_yaml(yaml_file_path):
    with open(str(yaml_file_path)) as yaml_file:
        return yaml.load(yaml_file)
