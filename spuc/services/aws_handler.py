import boto3

from spuc import utils


def create_user(user_config, service_config):
    user_config = \
        utils.convert_config_file(user_config)['aws']
    service_config = \
        utils.convert_config_file(service_config)['aws']

    client = boto3.client('iam', **service_config)
    return client.create_user(UserName=user_config['UserName'])
