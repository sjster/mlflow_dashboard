import pandas as pd
import requests
import pickle
import configparser
import os
import read_credentials

def get_credentials(credentials_path):
        TOKEN = read_credentials.get_credentials(credentials_path)
        print('Token is ',TOKEN)
        return(TOKEN)


def get_request_data(credentials_path):
    TOKEN = get_credentials(credentials_path)
    params = {"page": "1", "per_page": "100"}
    headers = {"Accept": "application/vnd.github.v3+json"}
    auth = ('sjster', TOKEN)
    return(headers, params, auth)


def get_requests(timeline_url, headers, params, auth):
    r = requests.get(timeline_url, headers=headers, params=params, auth=auth)
    print('Rate limit info - remaining ', r.headers['X-RateLimit-Remaining'])
    if(r.status_code != 403 and r.json != []):
        df = pd.DataFrame.from_records(r.json())
        if('created_at' in df.columns):
            ret_data = {'comment_dates': df['created_at'].values, 'comment_events': df['event'].values}
            return(ret_data)
        else:
            return(None)
    else:
        print('Status code ', r.status_code)
        raise Exception('API limit reached')


def get_issue_comments(credentials_path, TEST=False):
    headers, params, auth = get_request_data(credentials_path)

    df = pd.read_json('data/ingestion_issues.json')
    df_with_comments = df[df['comments'] > 0]
    if(TEST):
        df_with_comments = df_with_comments[0:5]
    print('Number of issues with comments ',len(df_with_comments))

    #df_with_comments['comments_history'] = df_with_comments['timeline_url'].apply(lambda x: get_requests(x))
    #df_with_comments[['number','id','comments_history']].to_json('comments_history.json')
    #ret_data = df[df['number'] == 1009]['timeline_url'].apply(lambda x: get_requests(x))
    # ISSUES - SCALABILITY - this method is unlikely to scale because of timeout issues and API rate limits
    comments_list = []
    for index, elem in df_with_comments.iterrows():
        print('Row ',index)
        try:
            ret_value = get_requests(elem['timeline_url'], headers, params, auth)
            comments_list.append((elem['number'], elem['id'], elem['created_at'], ret_value))
        except Exception as e:
            print('Exception ',e)
            print('Length of list ',len(comments_list))
            if(len(comments_list) > 0):
                print('Writing out file for comments')
                with open('data/comments_list.txt','wb') as f:
                    pickle.dump(comments_list, f)
            raise Exception(e)

    print("Done")
    with open('data/comments_list.txt','wb') as f:
        pickle.dump(comments_list, f)

    return(0)


if __name__ == '__main__':
    return_val = get_issue_comments(credentials_path)
