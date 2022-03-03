import pandas as pd
import json
import requests


def get_metadata(query_url = 'https://api.github.com/repos/mlflow/mlflow'):

    r = requests.get(query_url)
    repo_data = r.json()
    if(r.status_code == 200):
        print(repo_data['created_at'])
        print(repo_data['updated_at'])
        print(repo_data['forks_count'])
        print(repo_data['open_issues'])
        print(repo_data['stargazers_count']) # stars
        print(repo_data['subscribers_count']) # watchers

        repo_metadata = {'created_at': repo_data['created_at'],
                        'updated_at': repo_data['updated_at'],
                        'forks_count': repo_data['forks_count'],
                        'open_issues': repo_data['open_issues'],
                        'starred': repo_data['stargazers_count'],
                        'watchers': repo_data['subscribers_count']}

        with open('data/mlflow_metadata.json','w') as f:
            json.dump(repo_metadata, f)

        return_val = 0
    else:
        return_val = r.status_code
        print('Request failed with error ',return_val)

    return(return_val)


if __name__ == '__main__':
    return_val = get_metadata()
