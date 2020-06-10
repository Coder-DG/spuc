import json
import unicodedata

import boto3
from botocore import exceptions as botocore_exceptions
from googleapiclient import http
from jira import exceptions, JIRA

import aws_handler
import gapps_handler
import github_handler
import jira_handler
from spuc import utils

RESULT_INDEXES = {
    'username': 1,
    'first_name': 2,
    'last_name': 3,
    'job_description': 4,
    'mobile_number': 7,
    'direct_manager': 9,
    'country': 17,
    'email_domain': 18,
    'github_username': 19,
    'github_organization': 20,
    'created_email_addr': 25,
    'user_row': 26
}
SERVICES_CREATE_METHODS = {
    'aws': aws_handler,
    'gapps': gapps_handler,
    'github': github_handler,
    'jira': jira_handler
}

logger = utils.logger


def create_users(service_config, service_name):
    service_config_holder = utils.convert_config_file(service_config)
    gapps_config = service_config_holder['gapps']
    script_config = service_config_holder['script']
    endpoint_service_config = service_config_holder[service_name]

    response = \
        get_script_result(
                gapps_config,
                script_config,
                service_name
        )['response']['result']
    decoded_response = unicodedata.normalize('NFKD', response).encode(
            'ascii',
            'ignore')
    user_details = json.loads(decoded_response)
    user_configs = _construct_user_configs(
            user_details,
            endpoint_service_config,
            service_name
    )
    if len(user_configs) != 0:
        counter = 0
        for user_config in user_configs:

            if service_name == 'github':
                getattr(SERVICES_CREATE_METHODS[service_name], 'invite_user')(
                        {service_name: user_config},
                        {service_name: endpoint_service_config}
                )
            else:
                getattr(SERVICES_CREATE_METHODS[service_name], 'create_user')(
                        {service_name: user_config},
                        {service_name: endpoint_service_config}
                )
            mark_as_created(
                    user_details[counter][RESULT_INDEXES['user_row']],
                    service_config,
                    script_config,
                    service_name
            )
            if service_name == 'gapps':
                save_created_email(
                        user_details[counter][RESULT_INDEXES['user_row']],
                        user_config['primaryEmail'],
                        gapps_config,
                        script_config
                )
            counter += 1
    else:
        logger.info('Nothing to create')

    return user_configs


def _construct_user_configs(user_details, service_config, service_name):
    user_construct_methods = {
        'aws': _construct_aws_user_configs,
        'gapps': _construct_gapps_user_configs,
        'github': _construct_github_user_configs,
        'jira': _construct_jira_user_configs
    }

    kwargs = {
        'user_details': user_details,
        'service_config': service_config
    }
    return user_construct_methods[service_name](**kwargs)


def _construct_aws_user_configs(**kwargs):
    user_configs = []
    for user in kwargs['user_details']:
        user_configs.append(
                {
                    'UserName':
                        _get_available_username(
                                first_name=user[RESULT_INDEXES['first_name']],
                                last_name=user[RESULT_INDEXES['last_name']],
                                service_config=kwargs['service_config'],
                                service_name='aws'
                        ),
                    'Password': utils.gen_password()
                }
        )
    return user_configs


def _construct_gapps_user_configs(**kwargs):
    user_configs = []
    for user in kwargs['user_details']:
        user_configs.append({
            'primaryEmail': _get_available_username(
                    first_name=user[RESULT_INDEXES['first_name']],
                    last_name=user[RESULT_INDEXES['last_name']],
                    domain=user[RESULT_INDEXES['email_domain']],
                    service_config=kwargs['service_config'],
                    service_name='gapps'
            ),
            'name': {
                'givenName': user[RESULT_INDEXES['first_name']],
                'familyName': user[RESULT_INDEXES['last_name']],
                'fullName': '{0} {1}'.format(
                        user[RESULT_INDEXES['first_name']],
                        user[RESULT_INDEXES['last_name']])
            },
            'relations': [
                {
                    'value': user[RESULT_INDEXES['direct_manager']],
                    'type': 'manager'
                }
            ],
            'phones': user[RESULT_INDEXES['mobile_number']],
            'addresses':
                {
                    'type': 'work',
                    'country': user[RESULT_INDEXES['country']]
                },
            'password': utils.gen_password()
        }
        )
    return user_configs


def _construct_github_user_configs(**kwargs):
    user_configs = []
    for user in kwargs['user_details']:
        user_configs.append(
                {
                    'username':
                        user[RESULT_INDEXES['github_username']],
                    'organization':
                        user[RESULT_INDEXES['github_organization']]
                }
        )
    return user_configs


def _construct_jira_user_configs(**kwargs):
    user_configs = []
    for user in kwargs['user_details']:
        user_configs.append(
                {
                    'username':
                        _get_available_username(
                                first_name=user[RESULT_INDEXES['first_name']],
                                last_name=user[RESULT_INDEXES['last_name']],
                                service_config=kwargs['service_config'],
                                service_name='jira'
                        ),
                    'fullname':
                        user[RESULT_INDEXES['first_name']] +
                        ' ' +
                        user[RESULT_INDEXES['last_name']],
                    'password': utils.gen_password(),
                    'email': user[RESULT_INDEXES['created_email_addr']]
                }
        )
    return user_configs


def _get_available_username(first_name, last_name, service_config,
                            service_name, domain=None):
    get_available_name_methods = {
        'aws': _get_available_aws_username,
        'gapps': _get_available_gapps_username,
        'jira': _get_available_jira_username
    }

    kwargs = {
        'first_name': first_name,
        'last_name': last_name,
        'service_config': service_config,
        'domain': domain
    }

    return get_available_name_methods[service_name](**kwargs)


def _get_available_aws_username(**kwargs):
    desired_username = kwargs['first_name']
    client = boto3.client('iam', **kwargs['service_config'])
    try:
        client.get_user(UserName=desired_username)
        for c in kwargs['last_name']:
            desired_username += c
            client.get_user(UserName=desired_username)
    except botocore_exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            return desired_username
        raise e

    raise Exception('No appropriate username was available')


def _get_available_gapps_username(**kwargs):
    desired_username = kwargs['first_name']
    suffix = '@' + kwargs['domain']
    service = utils.get_service(
            kwargs['service_config'],
            utils.GOOGLE_SCOPES,
            'admin',
            'directory_v1',
            'google'
    )
    cnt = 0
    try:
        service.users().get(
                userKey=desired_username + suffix).execute()
        for c in kwargs['last_name']:
            cnt += 1
            desired_username += c
            service.users().get(
                    userKey=desired_username + suffix).execute()
    except http.HttpError as e:
        if e.resp['status'] == '404':
            return desired_username + suffix
        if e.resp['status'] == '403':
            return _get_available_username(
                    desired_username,
                    kwargs['last_name'][cnt + 1:],
                    kwargs['domain'],
                    kwargs['service_config']
            )
        raise e

    raise Exception('No appropriate email address was available')


def _get_available_jira_username(**kwargs):
    desired_username = kwargs['first_name']
    jira = JIRA(options=kwargs['service_config']['jira_options'],
                basic_auth=(
                    kwargs['service_config']['username'],
                    kwargs['service_config']['password']
                ))
    try:
        jira.user(id=desired_username)
        for c in kwargs['last_name']:
            desired_username += c
            jira.user(id=desired_username)
    except exceptions.JIRAError as e:
        if e.status_code == 404:
            return desired_username
        raise e

    raise Exception('No appropriate username was available')


def get_script_result(service_config, script_config, service_name):
    service = utils.get_service(
            service_config,
            utils.GOOGLE_SCOPES,
            'script',
            'v1',
            'google'
    )

    request = {
        'function': script_config['get_api_method'],
        'parameters': service_name
    }

    response = service.scripts().run(
            body=request,
            scriptId=script_config['id']
    ).execute()

    if 'error' in response:
        # The API executed, but the script returned an error.
        error = response['error']['details'][0]
        raise Exception(
                "Script error! Message: {0}".format(error['errorMessage']))

    return response


def mark_as_created(user_row, service_config, script_config, service_name):
    service = utils.get_service(
            service_config,
            utils.GOOGLE_SCOPES,
            'script',
            'v1',
            'google'
    )

    request = {
        'function': script_config['post_api_method'],
        'parameters': [user_row, service_name]
    }
    response = service.scripts().run(
            body=request,
            scriptId=script_config['id']
    ).execute()

    if 'error' in response:
        # The API executed, but the script returned an error.
        error = response['error']['details'][0]
        raise Exception(
                "Script error! Message: {0}".format(error['errorMessage']))

    return response


def save_created_email(user_row, user_email, service_config, script_config):
    service = utils.get_service(
            service_config,
            utils.GOOGLE_SCOPES,
            'script',
            'v1',
            'google'
    )

    request = {
        'function': script_config['save_email_api_method'],
        'parameters': [user_row, user_email]
    }
    response = service.scripts().run(
            body=request,
            scriptId=script_config['id']
    ).execute()

    if 'error' in response:
        # The API executed, but the script returned an error.
        error = response['error']['details'][0]
        raise Exception(
                "Script error! Message: {0}".format(error['errorMessage']))

    return response
