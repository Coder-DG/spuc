import unittest
from click.testing import CliRunner

from spuc import spuc


class TestOAuth(unittest.TestCase):
    def test_get_credentials_with_correct_input(self):
        runner = CliRunner()
        result = runner.invoke(spuc.main, [
            'gapps',
            'create',
            '-c/home/david/development/creds/credentials.yaml',
            '-u/home/david/development/yamls/google_user.yaml'
        ])

        assert result.exit_code == 0


class TestJira(unittest.TestCase):
    def test_user_create_with_correct_input(self):
        runner = CliRunner()
        result = runner.invoke(spuc.main, [
            'jira',
            'create',
            '-c/home/david/development/creds/credentials.yaml',
            '-u/home/david/development/yamls/jira_user.yaml'
        ])

        assert result.exit_code == 0


class TestAWS(unittest.TestCase):
    def test_user_create_with_correct_input(self):
        runner = CliRunner()
        result = runner.invoke(spuc.main, [
            'aws',
            'create',
            '-c/home/david/development/creds/credentials.yaml',
            '-u/home/david/development/yamls/aws_user.yaml'
        ])

        assert result.exit_code == 0
