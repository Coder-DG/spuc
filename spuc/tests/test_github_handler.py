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

    @mock.patch('utils.convert_config_file')
    def test_missing_user_config_key(self, mock_convert_config_file_util):
        mock_convert_config_file_util.return_value = \
            self.return_bad_service_config

        self.assertRaises(
                utils.SpucException,
                github_handler.invite_user(
                        user_config='',
                        service_config='service_config'
                )
        )

    def return_bad_service_config(self, config):
        if config == 'service_config':
            return {}

        return {'github': ''}
