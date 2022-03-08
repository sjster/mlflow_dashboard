import pandas as pd
import requests
import pickle
import configparser
import os

TOKEN = 0

def get_credentials():
        global TOKEN
        config = configparser.RawConfigParser()
        path = os.path.join(os.path.expanduser('~'), '.github/credentials')
        config.read(path)
        token_read = config.get('default', 'personal_access_token')
        TOKEN = token_read

def get_requests(timeline_url):
    params = {"page": "1", "per_page": "100"}
    headers = {"Accept": "application/vnd.github.v3+json"}
    auth = ('sjster', TOKEN)

    r = requests.get(timeline_url, headers=headers, params=params, auth=auth)
    df = pd.DataFrame.from_records(r.json())
    if('created_at' in df.columns):
        ret_data = {'comment_dates': df['created_at'].values, 'comment_events': df['event'].values}
        return(ret_data)
    else:
        return(None)


get_credentials()
df = pd.read_json('data/ingestion_issues.json')
df_with_comments = df[df['comments'] > 0]

#df_with_comments['comments_history'] = df_with_comments['timeline_url'].apply(lambda x: get_requests(x))
#df_with_comments[['number','id','comments_history']].to_json('comments_history.json')
#ret_data = df[df['number'] == 1009]['timeline_url'].apply(lambda x: get_requests(x))
comments_list = []
for index, elem in df_with_comments.iterrows():
    try:
        ret_value = get_requests(elem['timeline_url'])
        comments_list.append((elem['number'], elem['id'], elem['created_at'], ret_value))
    except e:
        print('Exception ',e)
        print('Length of list ',len(comments_list))
        with open('data/comments_list.txt','wb') as f:
            pickle.dump(comments_list, f)

print("Done")
with open('data/comments_list.txt','wb') as f:
    pickle.dump(comments_list, f)
