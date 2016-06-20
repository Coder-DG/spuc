import unittest

import mock

from spuc import utils
from spuc.services import github_handler


class GitHubHandlerCase(unittest.TestCase):
    def test_none_user_config(self):
        self.assertRaises(
                utils.SpucException,
                github_handler.invite_user,
                user_config=None,
                service_config=''
        )

    def test_none_service_config(self):
        self.assertRaises(
                utils.SpucException,
                github_handler.invite_user,
                user_config='',
                service_config=None
        )

    @mock.patch('spuc.utils.convert_config_file')
    def test_missing_user_config_key(self, mock_convert_config_file_util):
        mock_convert_config_file_util.side_effect = \
            self.return_bad_user_config

        self.assertRaises(
                KeyError,
                github_handler.invite_user,
                user_config='user_config',
                service_config='service_config'

        )

    def return_bad_user_config(self, config):
        if config == 'user_config':
            return {}

        return {'github': ''}

    @mock.patch('spuc.utils.convert_config_file')
    def test_missing_service_config_key(self, mock_convert_config_file_util):
        mock_convert_config_file_util.side_effect = \
            self.return_bad_service_config

        self.assertRaises(
                KeyError,
                github_handler.invite_user,
                user_config='user_config',
                service_config='service_config'

        )

    def return_bad_service_config(self, config):
        if config == 'service_config':
            return {}

        return {'github': ''}

    def test_no_github_service_config_username(self):
        user_config = {'github': ''}
        service_config = {'github': {'password': ''}}
        self.assertRaises(
                KeyError,
                github_handler.invite_user,
                user_config=user_config,
                service_config=service_config

        )

    def test_no_github_user_config_organization(self):
        user_config = {'github': {'username': ''}}
        service_config = {'github': {'password': '', 'username': ''}}
        self.assertRaises(
                KeyError,
                github_handler.invite_user,
                user_config=user_config,
                service_config=service_config

        )
