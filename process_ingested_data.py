import pandas as pd

df = pd.read_json('ingestion_issues.json')
df_processed = df[['url', 'id', 'number', 'title', 'state', 'locked', \
                'assignee', 'assignees', 'comments', 'created_at', 'updated_at', 'closed_at', \
                'body', 'pull_request']]
df_processed['labels'] = df['labels'].apply(lambda x: [elem['name'] for elem in x])
df_processed['labels_description'] = df['labels'].apply(lambda x: [elem['description'] for elem in x])

df_processed.to_json('processed_issues.json')
