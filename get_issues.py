import requests
import pandas as pd
from pprint import pprint
import json
import read_credentials


def call_rest_api(i, query_url, headers, params, auth):
    params["page"] = str(i)
    r = requests.get(query_url, headers=headers, params=params, auth=auth)
    if(r.status_code != 403):
        return(r)
    else
        raise Exception('API limit reached')


def get_github_issues(credentials_path=None, TEST=False):
    query_url = f"https://api.github.com/repos/mlflow/mlflow/issues"
    params = {"page": "1", "per_page": "100"}
    headers = {"Accept": "application/vnd.github.v3+json"}
    TOKEN = read_credentials.get_credentials(credentials_path)
    auth = ('sjster', TOKEN)

    i = 1
    json_list = []
    DONE = False

    while(not DONE):
        r = call_rest_api(i, query_url, headers, params, auth)
        if(r.json()):
            json_list.extend(r.json())
            i = i + 1
            print("Page ",i)
            if(TEST):
                DONE = True
        else:
            DONE = True

    df = pd.DataFrame.from_records(json_list)
    if(len(df) != 0):
        df.to_json("data/ingestion_issues.json")
        print('Issues returned from data ingestion',len(df))
        return_val = 0
    else:
        reason = r.reason
        return_val = r.status_code
        print(f'No issues returned from ingestion with {return_val} and reason {reason}')

    return(return_val)


if __name__ == '__main__':
    get_github_issues()
