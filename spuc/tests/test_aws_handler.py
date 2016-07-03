import unittest

import mock
from mock.mock import MagicMock

from spuc import utils
from spuc.services import aws_handler


class AwsHandlerCase(unittest.TestCase):
    def test_none_user_config(self):
        self.assertRaises(
                utils.SpucException,
                aws_handler.create_user,
                user_config=None,
                service_config=''
        )

    def test_none_service_config(self):
        self.assertRaises(
                utils.SpucException,
                aws_handler.create_user,
                user_config='',
                service_config=None
        )

    @mock.patch('spuc.utils.convert_config_file')
    def test_missing_user_config_key(self, mock_convert_config_file_util):
        mock_convert_config_file_util.side_effect = \
            self.return_bad_user_config

        self.assertRaises(
                KeyError,
                aws_handler.create_user,
                user_config='user_config',
                service_config='service_config'

        )

    def return_bad_user_config(self, config):
        if config == 'user_config':
            return {}

        return {'aws': {}}

    @mock.patch('spuc.utils.convert_config_file')
    def test_missing_service_config_key(self, mock_convert_config_file_util):
        mock_convert_config_file_util.side_effect = \
            self.return_bad_service_config

        self.assertRaises(
                KeyError,
                aws_handler.create_user,
                user_config='user_config',
                service_config='service_config'

        )

    def return_bad_service_config(self, config):
        if config == 'service_config':
            return {}

        return {'aws': {}}

    def test_no_aws_service_config_aws_access_key_id(self):
        user_config = {'aws': {}}
        service_config = {'aws': {'aws_secret_access_key': 'AKIA'}}

        self.assertRaises(
                TypeError,
                aws_handler.create_user,
                user_config=user_config,
                service_config=service_config

        )

    def test_no_aws_service_config_aws_access_key_secret(self):
        user_config = {'aws': {}}
        service_config = {'aws': {'aws_access_key_id': 'AKIA'}}

        self.assertRaises(
                TypeError,
                aws_handler.create_user,
                user_config=user_config,
                service_config=service_config

        )

    def test_no_aws_user_config_username(self):
        user_config = {'aws': {}}
        service_config = {
            'aws': {
                'aws_secret_access_key': 'AKIA',
                'aws_access_key_id': 'AKIA'
            }
        }

        self.assertRaises(
                KeyError,
                aws_handler.create_user,
                user_config=user_config,
                service_config=service_config

        )

    @mock.patch('boto3.client')
    def test_no_aws_user_config_password(self):
        user_config = {'aws': {'UserName': 'user_name'}}
        service_config = {
            'aws': {
                'aws_secret_access_key': 'AKIA',
                'aws_access_key_id': 'AKIA'
            }
        }

        self.assertRaises(
                KeyError,
                aws_handler.create_user,
                user_config=user_config,
                service_config=service_config

        )
