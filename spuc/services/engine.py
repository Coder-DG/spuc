import getpass
import json

import aws
import github
import google
import jira_handler


def load_json(url):
    with open(url, 'r') as json_file:
        json_string = json.load(json_file)

    return json_string


def invite_user_github():
    username = raw_input('Enter username: ')
    password = getpass.getpass(prompt='Enter password: ')

    print github.invite_user(username=username, password=password)


def create_user_aws():
    print aws.create_user()


def create_user_google():
    response = google.create_user(
            load_json('/home/david/development/jsons/google_user.json'))

    print response


def create_user_jira():
    username = raw_input('Enter username: ')
    password = getpass.getpass(prompt='Enter password: ')
    new_user_dict = {
        'username': 'test_username',
        'email': 'test@gigaspaces.com'
    }
    response = jira_handler.create_user(
            new_user_dict,
            username=username,
            password=password
    )

    print response


def main():
    # create_user_google()
    # create_user_jira()
    # create_user_aws()
    invite_user_github()

if __name__ == '__main__':
    main()
