import unittest

import mock
from mock.mock import MagicMock

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

    def test_no_github_user_config_username(self):
        user_config = {'github': {'organization': ''}}
        service_config = {'github': {'password': '', 'username': ''}}
        self.assertRaises(
                KeyError,
                github_handler.invite_user,
                user_config=user_config,
                service_config=service_config

        )

    @mock.patch('requests.put')
    def test_response_with_correct_input(self, mock_put):
        user_config = {'github': {'organization': 'org', 'username': 'uname'}}
        service_config = {'github': {'username': 'uname', 'password': 'pwd'}}
        mock_put.return_value = MagicMock(status_code=200, text='txt')

        github_handler.invite_user(
                user_config=user_config,
                service_config=service_config
        )
        mock_put.assert_called_with(
                'https://api.github.com/orgs/'
                '{0}/memberships/{1}'.format(
                        'org',
                        'uname'
                ),
                auth=('uname', 'pwd')
        )

    @mock.patch('requests.put')
    def test_bad_responses(self, mock_put):
        user_config = {'github': {'organization': 'org', 'username': 'uname'}}
        service_config = {'github': {'username': 'uname', 'password': 'pwd'}}

        # Bad status_code
        mock_put.return_value = MagicMock(status_code=199, text='txt')
        self.assertRaises(
                RuntimeError,
                github_handler.invite_user,
                user_config=user_config,
                service_config=service_config
        )

        mock_put.return_value = MagicMock(status_code=300, text='txt')
        self.assertRaises(
                RuntimeError,
                github_handler.invite_user,
                user_config=user_config,
                service_config=service_config
        )

        # Bad reponse text
        mock_put.return_value = MagicMock(status_code=200, text=None)
        self.assertRaises(
                RuntimeError,
                github_handler.invite_user,
                user_config=user_config,
                service_config=service_config
        )

        mock_put.return_value = MagicMock(status_code=200, text='')
        self.assertRaises(
                RuntimeError,
                github_handler.invite_user,
                user_config=user_config,
                service_config=service_config
        )
