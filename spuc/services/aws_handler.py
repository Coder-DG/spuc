import boto3

from spuc import utils


def create_user(user_config, service_config):
    if not user_config:
        raise utils.SpucException('No user config was provided')
    if not service_config:
        raise utils.SpucException('No service config was provided')

    service_config = utils.convert_config_file(service_config)
    user_configs = utils.convert_config_file(user_config)

    try:
        aws_service_config = service_config['aws']
        user_config = user_configs['aws']
    except KeyError as exception:
        raise exception

    client = boto3.client('iam', **aws_service_config)
    return [
        client.create_user(
                UserName=user_config['UserName']
        ),
        client.update_login_profile(
                UserName=user_config['UserName'],
                Password=user_config['Password']
        )
    ]
