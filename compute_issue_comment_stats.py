import numpy as np
import pandas as pd
from dateutil import parser
import pytz
import pickle

def get_data():
    with open('data/comments_list.txt','rb') as f:
        data = pickle.load(f)
    return(data)

def compute_stats():
    issue_id_list = []
    issue_date_list = []
    time_first_response_list = []
    data = get_data()
    for elem in data:
        pos = np.where(elem[3]['comment_events'] == 'commented')
        comment_dates_parsed = elem[3]['comment_dates'][pos]
        issue_date = elem[2]
        first_comment_time = parser.parse(comment_dates_parsed[0])
        first_comment_time = first_comment_time.replace(tzinfo=pytz.utc)
        issue_id_list.append(elem[0])
        issue_date_list.append(issue_date)
        time_first_response_list.append(first_comment_time - issue_date)

    df = pd.DataFrame({'issue_id': issue_id_list, 'issue_date': issue_date_list, 'time_first_response': time_first_response_list})
    grouped_df_median = df[['issue_date','time_first_response']].set_index('issue_date').resample('M').median()
    grouped_df_mean = df[['issue_date','time_first_response']].set_index('issue_date').resample('M').mean()
    joined_df = grouped_df_mean.join(grouped_df_median, lsuffix='_mean', rsuffix='_median')
    joined_df.to_json('data/comment_first_response.json', orient='records')
    print('Written time to first response file ',len(joined_df))
    return(0)

if __name__ == '__main__':
    return_val = compute_stats()
