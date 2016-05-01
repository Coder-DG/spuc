import unittest
from click.testing import CliRunner

import spuc.spuc


class TestOAuth(unittest.TestCase):
    def test_get_credentials_with_correct_input(self):
        runner = CliRunner()
        result = runner.invoke(spuc.main, [
            'gapps',
            'create',
            '-p/home/david/development/creds/client_secret.json',
            '-u/home/david/development/jsons/google_user.json'
        ])

        assert result.exit_code == 0
