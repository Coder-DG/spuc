from spuc import utils


def create_user(user_config, service_config):
    if not user_config:
        raise utils.SpucException('No user config was provided')
    if not service_config:
        raise utils.SpucException('No service config was provided')

    service_config = utils.convert_config_file(service_config)
    user_configs = utils.convert_config_file(user_config)

    try:
        gapps_service_config = service_config['gapps']
        user_config = user_configs['gapps']
    except KeyError as exception:
        raise exception

    service = utils.get_service(
            gapps_service_config,
            utils.GOOGLE_SCOPES,
            'admin',
            'directory_v1',
            'google'
    )

    result = service.users().insert(body=user_config).execute()
    return result
