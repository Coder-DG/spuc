import os
import json

import sys
import yaml
import string
import random
import logging
import tempfile
import httplib2

from oauth2client import file
from oauth2client import tools
from oauth2client import client
from googleapiclient import discovery

APPLICATION_NAME = 'SPUC'
GOOGLE_SCOPES = [
    'https://www.googleapis.com/auth/admin.directory.user',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets'
]


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
        logging.debug('Storing credentials to ' + credential_path)
    return credentials


def create_credential_json(credential_dict):
    tmp_dir_path = tempfile.mkdtemp()
    file_path = tmp_dir_path + '_spuc_secret.json'
    with open(file_path, 'w') as output:
        json.dump(credential_dict, output)
    return file_path


def convert_file_to_yaml(yaml_file_path):
    with open(str(yaml_file_path)) as yaml_file:
        return yaml.load(yaml_file)


def convert_config_file(path):
    if path and isinstance(path, basestring) and os.path.isfile(path):
        return convert_file_to_yaml(path)
    return path


def gen_password(size=8, chars=string.ascii_letters + string.digits):
    if size <= 0:
        raise SpucException('Size must be greater than 0')

    return ''.join(random.choice(chars) for _ in range(size))


def get_service(service_config, scope, service_name, version, name_prefix):
    credentials = get_oauth_credentials(
            credential_config_dict=service_config,
            scopes=scope,
            name_prefix=name_prefix
    )

    http = credentials.authorize(httplib2.Http())
    return discovery.build(service_name, version, http=http)


def get_logger():
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger('spuc')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


logger = get_logger()


class SpucException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
