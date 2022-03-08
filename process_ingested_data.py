import pandas as pd

def process():
    df = pd.read_json('data/ingestion_issues.json')
    df_processed = df[['html_url', 'id', 'number', 'title', 'state', 'locked', \
                    'assignee', 'assignees', 'comments', 'created_at', 'updated_at', 'closed_at', \
                    'body', 'pull_request']]
    df_processed['labels'] = df['labels'].apply(lambda x: [elem['name'] for elem in x])
    df_processed['labels_description'] = df['labels'].apply(lambda x: [elem['description'] for elem in x])

    df_processed.to_json('data/processed_issues.json')
    return(0)

if __name__ == '__main__':
    ret = process()
    print('processed_issues.json written out ',ret)
