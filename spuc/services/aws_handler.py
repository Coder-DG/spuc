import boto3

from spuc import utils


def create_user(user_config, service_config):
    user_config = \
        utils.check_is_file_and_convert_from_yaml(user_config)['aws']
    service_config = \
        utils.check_is_file_and_convert_from_yaml(service_config)['aws']

    client = boto3.client('iam', **service_config)
    return client.create_user(UserName=user_config['UserName'])
