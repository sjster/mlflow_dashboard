import requests
import pandas as pd
from pprint import pprint
import json
import read_credentials

def call_rest_api(i, query_url, headers, params, auth):
    try:
        params["page"] = str(i)
        r = requests.get(query_url, headers=headers, params=params, auth=auth)
        return(r, True)
    except:
        return(r, False)

def get_contributors(credentials_path=None, TEST=False):
    query_url = f"https://api.github.com/repos/mlflow/mlflow/contributors"
    params = {"page": "1", "per_page": "100"}
    headers = {"Accept": "application/vnd.github.v3+json"}
    TOKEN = read_credentials.get_credentials(credentials_path)
    auth = ('sjster', TOKEN)

    i = 1
    json_list = []
    DONE = False

    while(not DONE):
        r = call_rest_api(i, query_url, headers, params, auth)
        if(r[1]):
            json_list.extend(r[0].json())
            i = i + 1
            print("Page ",i)
            if(TEST):
                DONE = True
        else:
            DONE = True

    df = pd.DataFrame.from_records(json_list)
    if(len(df) != 0):
        df.to_json("data/contributors.json")
        print('Contributors ',len(df))
        return_val = 0
    else:
        reason = r[0].reason
        return_val = r[0].status_code
        print(f'No issues returned from ingestion with {return_val} and reason {reason}')

    return(return_val)


if __name__ == '__main__':
    get_contributors()
