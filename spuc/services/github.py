import requests


def invite_user(username, password):
    response1 = requests.put(
            'https://api.github.com/orgs/test-github-dev-stuff/' +
            'memberships/username',
            auth=(username, password)
    )

    response2 = requests.put(
            'https://api.github.com/teams/2006458/members/username',
            auth=(username, password)
    )

    return response1.text, \
           response1.status_code, \
           response2.text, \
           response2.status_code
