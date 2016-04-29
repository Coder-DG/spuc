import httplib2
from googleapiclient import discovery


def create_user(user_json, credentials):

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('admin', 'directory_v1', http=http)

    result = service.users().insert(body=user_json).execute()
    return result
