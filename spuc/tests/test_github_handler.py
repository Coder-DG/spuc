import unittest

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
