import unittest
from click.testing import CliRunner

from spuc import spuc


class TestOAuth(unittest.TestCase):
    def test_get_credentials_with_correct_input(self):
        runner = CliRunner()
        result = runner.invoke(spuc.main, [
            'gapps',
            'create',
            '-c/home/david/development/creds/client_secret.json',
            '-j/home/david/development/jsons/google_user.json'
        ])

        assert result.exit_code == 0


class TestJira(unittest.TestCase):
    def test_user_create_with_correct_input(self):
        runner = CliRunner()
        result = runner.invoke(spuc.main, [
            'jira',
            'create',
            '-c/home/david/development/creds/jira_creds.json',
            '-j/home/david/development/jsons/jira_user.json',
            '-o/home/david/development/creds/jira_options.json'
        ])

        assert result.exit_code == 0
