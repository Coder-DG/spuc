import click
import logging

import utils
from services import gapps_handler, jira_handler, aws_handler, \
    github_handler, gapps_script_handler

logger = utils.logger


class Spuc(object):
    SERVICES_MODULES = {
        'aws': aws_handler,
        'gapps': gapps_handler,
        'github': github_handler,
        'jira': jira_handler
    }

    def __init__(self, services_config, user_config):
        self.user_configs = utils.convert_config_file(user_config)
        self.services_config = \
            utils.convert_config_file(services_config)

    def create_all(self):
        # GAPPS mailbox must be create first for the others to run
        # service_names = ['gapps', 'aws', 'github', 'jira']

        if self.user_configs:
            logger.info('Creating users from config file...')

            def create_user(service_name):
                logger.info('Creating user for the {0} service...'.format(
                        service_name)
                )

                users_config = self.user_configs[service_name]
                if service_name == 'github':
                    for user_config in users_config:
                        getattr(
                                self.SERVICES_MODULES[service_name],
                                'invite_user'
                        )(
                                {service_name: user_config},
                                self.services_config
                        )
                else:
                    for user_config in users_config:
                        getattr(
                                self.SERVICES_MODULES[service_name],
                                'create_user'
                        )(
                                {service_name: user_config},
                                self.services_config
                        )

            create_user('gapps')
            create_user('aws')
            create_user('github')
            create_user('jira')

        else:
            logger.info('Fetching users\' data from gapps script API...')

            self.user_configs = {}

            def create_user_from_script(service_name):
                logger.info('Creating user for the {0} service...'.format(
                        service_name)
                )

                user_config = gapps_script_handler.create_users(
                        self.services_config,
                        service_name
                )
                self.user_configs[service_name] = user_config

            create_user_from_script('gapps')
            create_user_from_script('aws')
            create_user_from_script('github')
            create_user_from_script('jira')

    def print_passwords(self):
        if self.user_configs:
            if len(self.user_configs) != 0:
                logger.info('Printing passwords...')

                for service_name, users_config in \
                        self.user_configs.iteritems():
                    for user_config in users_config:
                        password = \
                            self._extract_password(
                                    user_config,
                                    service_name
                            )
                        logger.info('\t{0} service: {1}'.format(
                                service_name,
                                password
                        ))
            else:
                logger.info('Nothing to do here')
        else:
            raise utils.SpucException('No user config was provided')

    def _extract_password(self, user_config, service_name):
        methods = {
            'aws': self._extract_from_aws,
            'gapps': self._extract_from_gapps,
            'jira': self._extract_from_jira,
        }

        if service_name == 'github':
            return 'Invite has been sent'

        return methods[service_name](**user_config)

    @staticmethod
    def _extract_from_aws(**kwargs):
        return kwargs['Password']

    @staticmethod
    def _extract_from_gapps(**kwargs):
        return kwargs['password']

    @staticmethod
    def _extract_from_jira(**kwargs):
        return kwargs['password']


@click.group()
def main():
    pass


@main.command(name='create-all')
@click.option('-c', '--config-path',
              help='The path to the config file.',
              required=True)
@click.option('-u', '--user-config-path',
              help='The path to the user yaml config file.')
@click.option('-p', '--without-passwords',
              is_flag=True,
              default=True,
              help='The path to the user yaml config file.')
def create_all_users(config_path, user_config_path, without_passwords):
    spuc = Spuc(config_path, user_config_path)
    spuc.create_all()
    if without_passwords:
        spuc.print_passwords()


@main.group()
def gapps():
    pass


@gapps.command(name='create')
@click.option('-c', '--config-path',
              help='The path to the config file.',
              required=True)
@click.option('-u', '--user-config-path',
              help='The path to the user yaml config file.')
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
              help='The path to the user config file.')
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
              help='The path to the user yaml config file.')
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
              help='The path to the user config file.')
def invite_user_github(config_path, user_config_path):
    response = github_handler.invite_user(
            user_config_path,
            config_path
    )
    logging.debug(response)
