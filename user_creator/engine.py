import requests
import getpass
import json

username = raw_input('Enter username: ')
password = getpass.getpass(prompt='Enter password: ')
user = ''

with open('~/development/jsons/user.json', 'r') as user_json_file:
    user = json.dump(user_json_file)

requests.post('https://www.googleapis.com/admin/directory/v1/users',
              auth=(username, password))