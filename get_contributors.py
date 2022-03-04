import requests
import pandas as pd
from pprint import pprint
import json


def get_contributors():

    def call_rest_api(i):
        try:
            params["page"] = str(i)
            r = requests.get(query_url, headers=headers, params=params)
            return(r)
        except:
            return(False)

    query_url = f"https://api.github.com/repos/mlflow/mlflow/contributors"
    params = {
        "page": "1",
        "per_page": "100"
    }

    headers = {"Accept": "application/vnd.github.v3+json"}
    i = 1
    json_list = []
    DONE = False

    while(not DONE):
        r = call_rest_api(i)
        if(r):
            json_list.extend(r.json())
            i = i + 1
            print("Page ",i)
        else:
            DONE = True

    df = pd.DataFrame.from_records(json_list)
    if(len(df) != 0):
        df.to_json("data/contributors.json")
        print('Contributors ',len(df))
        return_val = 0
    else:
        print('No issues returned from ingestion')
        return_val = 'NO DATA'

    return(return_val)


if __name__ == '__main__':
    get_contributors()
