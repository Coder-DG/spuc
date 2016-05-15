import click
import logging

import utils
from services import gapps_handler, jira_handler, aws_handler, github_handler


class Spuc(object):
    def __init__(self, services_config, user_config):
        self.user_config = utils.convert_config_file(
                user_config)
        self.services_config = \
            utils.convert_config_file(services_config)

    def create_all(self):
        response = gapps_handler.create_user(
                self.user_config['gapps'],
                self.services_config['gapps']
        )
        logging.debug(response)

        response = jira_handler.create_user(
                self.user_config['jira'],
                self.services_config['jira']
        )
        logging.debug(response)

        response = aws_handler.create_user(
                self.user_config['aws'],
                self.services_config['aws']
        )
        logging.debug(response)

        response = github_handler.invite_user(
                self.user_config['github'],
                self.services_config['github']
        )
        logging.debug(response)


@click.group()
def main():
    pass

@main.command(name='create-all')
@click.option('-c', '--config-path',
              help='The path to the config file.',
              required=True)
@click.option('-u', '--user-config-path',
              help='The path to the user yaml config file.',
              required=True)
def create_all_users(config_path, user_config_path):
    spuc = Spuc(config_path, user_config_path)
    spuc.create_all()


@main.group()
def gapps():
    pass


@gapps.command(name='create')
@click.option('-c', '--config-path',
              help='The path to the config file.',
              required=True)
@click.option('-u', '--user-config-path',
              help='The path to the user yaml config file.',
              required=True)
def create_user_google(config_path, user_config_path):
    response = gapps_handler.create_user(
            user_config_path,
            config_path
    )
    logging.debug(response)


@main.group()
def jira():
    pass


@jira.command(name='create')
@click.option('-c', '--config-path',
              help='The path to the config file.',
              required=True)
@click.option('-u', '--user-config-path',
              help='The path to the user config file.',
              required=True)
def create_user_jira(config_path, user_config_path):
    response = jira_handler.create_user(
            user_config_path,
            config_path
    )

    logging.debug(response)


@main.group()
def aws():
    pass


@aws.command(name='create')
@click.option('-c', '--config-path',
              help='The path to the config file.',
              required=True)
@click.option('-u', '--user-config-path',
              help='The path to the user yaml config file.',
              required=True)
def create_user_aws(config_path, user_config_path):
    response = aws_handler.create_user(
            user_config_path,
            config_path
    )
    logging.debug(response)


@main.group()
def github():
    pass


@github.command(name='invite')
@click.option('-c', '--config-path',
              help='The path to the config file.',
              required=True)
@click.option('-u', '--user-config-path',
              help='The path to the user config file.',
              required=True)
def invite_user_github(config_path, user_config_path):
    response = github_handler.invite_user(
            user_config_path,
            config_path
    )
    logging.debug(response)
