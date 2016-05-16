import unittest
from click.testing import CliRunner

from spuc import spuc, services, utils


class TestOAuth(unittest.TestCase):
    def test_get_credentials_with_correct_input(self):
        runner = CliRunner()
        result = runner.invoke(spuc.main, [
            'create-all',
            '-c/home/david/development/creds/credentials.yaml'
        ])

        assert result.exit_code == 0


class TestJira(unittest.TestCase):
    def test_user_create_with_correct_input(self):
        runner = CliRunner()
        result = runner.invoke(spuc.main, [
            'jira',
            'create',
            '-c/home/david/development/creds/credentials.yaml',
        ])

        assert result.exit_code == 0


class TestAWS(unittest.TestCase):
    def test_user_create_with_correct_input(self):
        runner = CliRunner()
        result = runner.invoke(spuc.main, [
            'aws',
            'create',
            '-c/home/david/development/creds/credentials.yaml'
        ])

        assert result.exit_code == 0


class TestGitHub(unittest.TestCase):
    def test_user_create_with_correct_input(self):
        runner = CliRunner()
        result = runner.invoke(spuc.main, [
            'github',
            'invite',
            '-c/home/david/development/creds/credentials.yaml'
        ])

        assert result.exit_code == 0


class TestDummy(unittest.TestCase):
    def test_app_script_response(self):
        service_config = utils.convert_file_to_yaml(
                '/home/david/development/creds/credentials.yaml'
        )['gapps']
        script_config = service_config.pop('script')
        result = utils.mark_as_created(
                '14',
                service_config,
                script_config

        )

        print result
