import configparser
import requests
import os

def get_credentials(path):
    config = configparser.RawConfigParser()
    #path = os.path.join(os.path.expanduser('~'), path)
    print('credentials path is ',path)
    config.read(path)
    token_read = config.get('default', 'personal_access_token')
    return(token_read)


def test_rate_limiting(path, user):
    url = 'https://api.github.com/users/octocat'
    params = {"page": "1", "per_page": "100"}
    headers = {"Accept": "application/vnd.github.v3+json"}
    TOKEN = get_credentials(path)
    auth = (user, TOKEN)
    r = requests.get(url, headers=headers, params=params, auth=auth)
    print('Request status ', r.status_code)
    print('Header info ', r.headers)
