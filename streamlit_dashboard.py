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
    with open('data/mlflow_metadata.json','r') as f:
        m = json.load(f)
    return(m)

def get_contributors():
    with open('data/contributors.json','r') as f:
        data = json.load(f)
    return(data['login'])

def get_phrases():
    with open('data/nounphrase_dict.json','r') as f:
        nounphrases = json.load(f)
    with open('data/verbphrase_dict.json','r') as f:
        verbphrases = json.load(f)
    nounphrases_df = pd.Series(nounphrases)
    nounphrases_df.sort_values(inplace=True, ascending=False)
    verbphrases_df = pd.Series(verbphrases)
    verbphrases_df.sort_values(inplace=True, ascending=False)
    return(nounphrases_df, verbphrases_df)

def resample_based_on_label(val):
    vals_over_time = labels_exploded[labels_exploded['labels'] == val][['created_at', 'labels']]
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
df = pd.read_json('data/processed_issues_entities.json')
df = process_pull_requests(df)
mlflow_metrics = get_mlflow_metrics()
nounphrases_df, verbphrases_df = get_phrases()
contributors = get_contributors()

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
col_metric1, col_metric2, col_metric3, col_metric4, col_metric5 = st.columns([1,1,1,1,1])
with col_metric1:
    st.metric('Number of issues',len(df))

with col_metric2:
    st.metric('Forks', mlflow_metrics['forks_count'])

with col_metric3:
    st.metric('Stars',mlflow_metrics['starred'])

with col_metric4:
    st.metric('Watchers',mlflow_metrics['watchers'])

with col_metric5:
    st.metric('Contributors',len(contributors))

# -------------------- Bugs, issues, enhancements, comments over time ------------------ #
col_bugs, col_issues = st.columns([1,1])

with col_issues:
    issues_by_week = df.set_index('created_at').resample(AGGREGATION_PERIOD).count()['id']
    issues_by_week.rename('Issues', inplace=True)
    fig = px.line(issues_by_week, title='Number of issues and comments by month')

    comments_by_week = df.set_index('created_at').resample(AGGREGATION_PERIOD).agg({'comments': 'sum'})
    fig2 = px.line(comments_by_week, title='Number of comments by month')
    fig.add_trace(fig2['data'][0])
    fig['data'][0].line.color = 'red'
    st.plotly_chart(fig)

labels_exploded = df.explode('labels')[['created_at','labels','entities']]
with col_bugs:
    fig = px.area(resample_based_on_label('bug'), title="Bug/enhancements/integrations by month")
    fig2 = px.area(resample_based_on_label('enhancement'), title="Bugs over time")
    fig3 = px.area(resample_match_label_pattern('integration'))
    fig4 = px.area(resample_based_on_label('rn/bug-fix'), title="Bug fixes over time")
    fig.add_trace(fig2['data'][0])
    fig.add_trace(fig3['data'][0])
    fig.add_trace(fig4['data'][0])
    fig['data'][0].line.color ='red'
    fig['data'][1].line.color = 'green'
    fig['data'][2].line.color = 'cyan'
    st.plotly_chart(fig)

# --------------------- Pie charts fpr state, locked and PRs --------------------#
st.subheader('Proportion of issues')

col1, col2, col3 = st.columns([1,1,1])

with col1:
    res = df['state'].value_counts()
    st.plotly_chart(px.pie(values=res.values, labels=res.index, title='State of issues'))

with col2:
    res = df['locked'].value_counts()
    st.plotly_chart(px.pie(values=res.values, labels=res.index, title='What % of issues are locked?'))

with col3:
    res = df['processed_pull_request'].value_counts()
    st.plotly_chart(px.pie(values=res.values, labels=res.index, title='Pull requests as % of total number of issues '))

# ---------------------- Histogram of issue labels and comments -------------------- #

st.subheader('Distribution of labels and comments')
col_labels, col_hist = st.columns([1,1])

with col_labels:
    label_count = df.explode('labels')['labels'].value_counts()
    st.plotly_chart(px.bar(label_count, title='Distribution of issue labels') )

with col_hist:
    comments_hist = px.histogram(df, 'comments', title="Distribution of comments")
    st.plotly_chart(comments_hist)

# ----------------------- Entities -------------------- #

st.subheader('Entities from titles - feature requests')
col_chart, col_dataframe = st.columns([1,1])

with col_chart:
    entities_count = labels_exploded[labels_exploded['labels'] == 'enhancement'].explode('entities')['entities'].value_counts()
    st.text('Top 50 entites in feature request titles')
    st.plotly_chart(px.bar(entities_count[0:50], orientation='h').
            update_layout(width=800, height=1200, yaxis={'categoryorder':'total ascending'}))

with col_dataframe:
    st.text('Full list of entity counts from feature request titles (scrollable)')
    st.dataframe(entities_count, height=1200)


col_noun, col_verb = st.columns([1,1])

with col_noun:
    st.text('Noun phrases in title')
    st.plotly_chart(px.bar(nounphrases_df.iloc[0:70], orientation='h').
                        update_layout(width=800, height=1200,  yaxis={'categoryorder':'total ascending'}))

with col_verb:
    st.text('Verb phrases in title')
    st.plotly_chart(px.bar(verbphrases_df.iloc[0:70], orientation='h').
                        update_layout(width=800, height=1200,  yaxis={'categoryorder':'total ascending'}))
