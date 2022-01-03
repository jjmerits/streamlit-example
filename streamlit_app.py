import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
from datetime import datetime, timezone
import seaborn as sns
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"

import plotly.graph_objects as go
import pymongo
import json
import requests

import gnews

import pytz
import time

#url = 'https://raw.githubusercontent.com/jjmerits/Dashboard/main/test_df_all.csv'
#test_df = pd.read_csv(url)

#name_list = test_df['Name'].unique().tolist()
#df = test_df[test_df['Name'] == name_list[4]]


#df['date'] = df['date'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S').strftime('%Y/%m/%d'))
#df.set_index("date", inplace = True)


st.set_page_config(layout='wide')
#fig = go.Figure()
#fig.add_trace(go.Bar(x=df[['actual']].index,y=df['actual'].to_list(),name='actual'))
#fig.add_trace(go.Bar(x=df[['actual']].index,y=df['forecast'].to_list(),name='forecast'))
#fig.update_layout(barmode='group',title=name_list[4], yaxis=dict(title = 'y/y %'))

#st.plotly_chart(fig,use_container_width=True)




#plot graph
def plot_graph(x,y=""):
  df_x = df[(df['event'] == x) | (df['event'] == y)]
  df_x = df_x.loc[df_x[['date','actual','forecast']].drop_duplicates().index]
  df_x.sort_values('date', inplace = True)
  df_x.set_index("date", inplace = True)
  fig = go.Figure()
  fig.add_trace(go.Bar(x=df_x[['actual']].index,y=df_x['actual'].to_list(),name='actual'))
  fig.add_trace(go.Bar(x=df_x[['actual']].index,y=df_x['forecast'].to_list(),name='forecast'))
  fig.update_layout(barmode='group',title=x, yaxis=dict(title = '')) #title=x+" "+df_x['currency'].values[1]
  #fig.show()
  st.plotly_chart(fig,use_container_width=True)



########################## #############################################################

def tz_diff(date, tz1, tz2):
    '''
    Returns the difference in hours between timezone1 and timezone2
    for a given date.
    '''
    date = pd.to_datetime(date)
    return (tz1.localize(date) -
            tz2.localize(date).astimezone(tz1)) \
               .seconds/3600
est = pytz.timezone('US/Eastern')
seo = pytz.timezone('Asia/Seoul')
time_diff = tz_diff(datetime.today().strftime('%Y-%m-%d'), est, seo)
est_time = datetime.today().astimezone(seo).astimezone(est).strftime('%d/%m/%y %H:%M:%S')
seo_time = datetime.today().astimezone(seo).strftime('%d/%m/%y %H:%M:%S')
st.header('News Flow (TimeZone = US/Eastern)')
st.write(f'Last updated time (US/EST): {est_time} / (Asia/Seoul):{seo_time}')

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = link.split('=')
    return f'<a target="_blank" href="{link}">{"link"}</a>'

def tz_diff(date, tz1, tz2):
    '''
    Returns the difference in hours between timezone1 and timezone2
    for a given date.
    '''
    date = pd.to_datetime(date)
    return (tz1.localize(date) -
            tz2.localize(date).astimezone(tz1)) \
               .seconds/3600
  
def gnews_html(q_str, cn='US', la='english'):
  st.write(q_str)
  google_news = gnews.GNews()
  google_news.country = cn
  google_news.language = la
  google_news.period = '24h'
  google_news.results = 30
  df = google_news.get_news(q_str)
  df = pd.DataFrame.from_records(df)
  df = df.reset_index().rename({'index':'importance'}, axis = 'columns')
  df['published date'] = df['published date'].apply(lambda x: datetime.strptime(x, '%a, %d %b %Y %H:%M:%S %Z').replace(tzinfo=timezone.utc))
  df['published date'] = df['published date'].dt.tz_convert('US/Eastern')
  #df['published date'] = df['published date'].apply(lambda x: x.strftime('%d/%m/%y %H:%M:%S'))
  df['published date'] = datetime.today().astimezone(seo).astimezone(est) - df['published date']
  df['published date'] = df['published date'].apply(lambda x: int(x.total_seconds()//3600))
  df.rename(columns={'published date': 'hour ago'}, inplace = True)
    
  df.sort_values('importance', inplace = True, ascending = True)
  df.drop(['description','publisher'], axis=1, inplace = True)
  # link is the column with hyperlinks
  df['url'] = df['url'].apply(make_clickable)
  #df.reset_index(drop=True, inplace=True)
  df = df.iloc[0:30,].to_html(escape=False,index=False)
  st.write(df, unsafe_allow_html=True)
##########################  
col1, col2 = st.columns(2)
with col1:
  gnews_html("tesla TSLA","US")
  
with col2:
  gnews_html("테슬라","KR", "ko")
##########################
col1, col2 = st.columns(2)
with col1:
  gnews_html("META FB","US")
  
with col2:
  gnews_html("s&p 500","US")
##########################
col1, col2 = st.columns(2)
with col1:
  gnews_html("nasdaq","US")
  
with col2:
  gnews_html("Dow 30","HK")
##########################


