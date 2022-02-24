import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import time
from datetime import datetime

st.set_page_config(layout='wide')

def process_pull_requests(df):
    # Verify data quality for no pull request == '<NA>'
    df['processed_pull_request'] = df['pull_request'].apply(lambda x: 0 if not x else 1)
    return(df)

def get_mlflow_metrics():
    with open('mlflow_metadata.json','r') as f:
        m = json.load(f)
    return(m)

def resample_based_on_label(val):
    vals_over_time = labels_exploded[labels_exploded['labels'] == val]
    vals_over_time_resampled = vals_over_time.set_index('created_at').resample(AGGREGATION_PERIOD).count()
    vals_over_time_resampled.rename(columns={"labels": val}, inplace=True)
    return(vals_over_time_resampled)

def resample_match_label_pattern(val):
    labels_exploded_dropna = labels_exploded.dropna(how='any')
    vals_over_time = labels_exploded_dropna[labels_exploded_dropna['labels'].str.contains(val, regex=False)]
    vals_over_time_resampled = vals_over_time.set_index('created_at').resample(AGGREGATION_PERIOD).count()
    vals_over_time_resampled.rename(columns={"labels": val}, inplace=True)
    return(vals_over_time_resampled)


AGGREGATION_PERIOD = 'M'
df = pd.read_json('processed_issues.json')
df = process_pull_requests(df)
mlflow_metrics = get_mlflow_metrics()

st.title("GitHub stats for MLflow")
st.subheader("All issues ")
st.dataframe(df)

# ------------------- Filter based on slider values --------------------#
date_vals = st.slider(
     "Date range: please drag the slider to the desired range",
     df['created_at'].min().to_pydatetime(),
     df['created_at'].max().to_pydatetime(),
     ( df['created_at'].min().to_pydatetime(), df['created_at'].max().to_pydatetime()),
     step = pd.Timedelta(days=15)
     )

print("Slider values ",date_vals[0])

df = df[df['created_at'] > date_vals[0]]

# ------------------- Metrics ----------------- #
col_metric1, col_metric2, col_metric3, col_metric4 = st.columns([1,1,1,1])
with col_metric1:
    st.metric('Number of issues',len(df))

with col_metric2:
    st.metric('Forks', mlflow_metrics['forks_count'])

with col_metric3:
    st.metric('Stars',mlflow_metrics['starred'])

with col_metric4:
    st.metric('Watchers',mlflow_metrics['watchers'])

# -------------------- Bugs, issues, enhancements, comments over time ------------------ #

col_bugs, col_issues = st.columns([1,1])

with col_issues:
    issues_by_week = df.set_index('created_at').resample(AGGREGATION_PERIOD).count()['id']
    issues_by_week.rename('Issues', inplace=True)
    fig = px.area(issues_by_week, title='Number of issues and comments by month')

    comments_by_week = df.set_index('created_at').resample(AGGREGATION_PERIOD).agg({'comments': 'sum'})
    fig2 = px.area(comments_by_week, title='Number of comments by month')
    fig.add_trace(fig2['data'][0])
    fig['data'][0].line.color = 'red'
    st.plotly_chart(fig)

labels_exploded = df.explode('labels')[['created_at','labels']]
with col_bugs:
    fig = px.area(resample_based_on_label('bug'), title="Bug/enhancements/integrations by month")
    fig2 = px.area(resample_based_on_label('enhancement'), title="Bugs over time")
    fig3 = px.area(resample_match_label_pattern('integration'))
    fig.add_trace(fig2['data'][0])
    fig.add_trace(fig3['data'][0])
    fig['data'][0].line.color ='red'
    fig['data'][1].line.color = 'green'
    st.plotly_chart(fig)

# --------------------- Pie charts fpr state, locked and PRs --------------------#

col1, col2, col3 = st.columns([1,1,1])

with col1:
    res = df['state'].value_counts()
    st.plotly_chart(px.pie(values=res.values, labels=res.index, title='State'))

with col2:
    res = df['locked'].value_counts()
    st.plotly_chart(px.pie(values=res.values, labels=res.index, title='Locked'))

with col3:
    res = df['processed_pull_request'].value_counts()
    st.plotly_chart(px.pie(values=res.values, labels=res.index, title='Pull requests as % of total number of issues '))

# ---------------------- Histogram of issue labels and comments -------------------- #

col_labels, col_hist = st.columns([1,1])

with col_labels:
    label_count = df.explode('labels')['labels'].value_counts()
    st.plotly_chart(px.bar(label_count, title='Distribution of issue labels') )

with col_hist:
    comments_hist = px.histogram(df, 'comments', title="Distribution of comments")
    st.plotly_chart(comments_hist)
