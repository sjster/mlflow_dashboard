import requests
import pandas as pd
from pprint import pprint
import json


def call_rest_api(i):
    try:
        params["page"] = str(i)
        r = requests.get(query_url, headers=headers, params=params)
        return(r)
    except:
        return(False)


query_url = f"https://api.github.com/repos/mlflow/mlflow/issues"
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
df.to_json("ingestion_issues.json")
print(df)
