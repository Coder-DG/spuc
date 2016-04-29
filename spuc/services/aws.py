import boto3
import yaml


def get_credentials():
    with open('/home/david/development/creds/aws_creds.yaml') \
            as aws_creds_file:
        credentials = yaml.load(aws_creds_file)

    return credentials


def create_user():
    credentials = get_credentials()

    client = boto3.client('iam', **credentials)

    return client.create_user(UserName='test-user_created_me')