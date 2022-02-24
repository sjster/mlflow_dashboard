import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout='wide')

def process_pull_requests(df):
    # Verify data quality for no pull request == '<NA>'
    df['processed_pull_request'] = df['pull_request'].apply(lambda x: 0 if not x else 1)
    return(df)

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
st.dataframe(df)
st.metric('Number of issues',len(df))
st.subheader('Issue date range ' + str(df['created_at'].min()) + ' ----> ' + str(df['created_at'].max()))

df = process_pull_requests(df)

col1, col2, col3 = st.columns([1,1,1])

with col1:
    res = df['state'].value_counts()
    st.plotly_chart(px.pie(values=res.values, labels=res.index, title='State'))

with col2:
    res = df['locked'].value_counts()
    st.plotly_chart(px.pie(values=res.values, labels=res.index, title='Locked'))

with col3:
    res = df['processed_pull_request'].value_counts()
    print(res)
    st.plotly_chart(px.pie(values=res.values, labels=res.index, title='Pull requests as % of total number of issues '))

col_hist, col_issues = st.columns([1,1])
with col_hist:
    comments_hist = px.histogram(df, 'comments', title="Distribution of comments")
    st.plotly_chart(comments_hist)

with col_issues:
    issues_by_week = df.set_index('created_at').resample(AGGREGATION_PERIOD).count()['id']
    issues_by_week.rename('Issues', inplace=True)
    fig = px.area(issues_by_week, title='Number of issues and comments by month')

    comments_by_week = df.set_index('created_at').resample(AGGREGATION_PERIOD).agg({'comments': 'sum'})
    fig2 = px.area(comments_by_week, title='Number of comments by month')
    fig.add_trace(fig2['data'][0])
    fig['data'][0].line.color = 'red'
    st.plotly_chart(fig)

label_count = df.explode('labels')['labels'].value_counts()
st.plotly_chart(px.bar(label_count, title='Distribution of issue labels') )

labels_exploded = df.explode('labels')[['created_at','labels']]

fig = px.area(resample_based_on_label('bug'), title="Bugs,enhancements,integrations over time")
fig2 = px.area(resample_based_on_label('enhancement'), title="Bugs over time")
fig3 = px.area(resample_match_label_pattern('integration'))
fig.add_trace(fig2['data'][0])
fig.add_trace(fig3['data'][0])
fig['data'][0].line.color ='red'
fig['data'][1].line.color = 'green'
st.plotly_chart(fig)
