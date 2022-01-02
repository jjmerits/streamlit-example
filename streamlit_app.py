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
  google_news.period = '12h'
  google_news.results = 30
  df = google_news.get_news(q_str)
  df = pd.DataFrame.from_records(df)
  df = df.reset_index().rename({'index':'importance'}, axis = 'columns')
  df['published date'] = df['published date'].apply(lambda x: datetime.strptime(x, '%a, %d %b %Y %H:%M:%S %Z').replace(tzinfo=timezone.utc))
  df['published date'] = df['published date'].dt.tz_convert('US/Eastern')
  df['published date'] = df['published date'].apply(lambda x: x.strftime('%d/%m/%y %H:%M:%S'))
  df.rename(columns={'published date': 'date (EST)'}, inplace = True)
    
  df.sort_values('date (EST)', inplace = True, ascending = False)
  df.drop(['description','publisher'], axis=1, inplace = True)
  # link is the column with hyperlinks
  df['url'] = df['url'].apply(make_clickable)
  #df.reset_index(drop=True, inplace=True)
  df = df.iloc[0:30,].to_html(escape=False,index=False)
  st.write(df, unsafe_allow_html=True)
##########################  
col1, col2 = st.columns(2)
with col1:
  gnews_html("Tesla TLSA","US")
  
with col2:
  gnews_html("Devon dvn")
##########################
col1, col2 = st.columns(2)
with col1:
  gnews_html("Facebook FB","US")
  
with col2:
  gnews_html("AUD currency","AU")
##########################
col1, col2 = st.columns(2)
with col1:
  gnews_html("Idian Rupee","IN")
  
with col2:
  gnews_html("Chinese Yuan","HK")
##########################
st.header(" ")
ts = time.time()
numofweek = str(datetime.fromtimestamp(ts).isocalendar()[1])
numofyear = str(datetime.fromtimestamp(ts).isocalendar()[0])
#url = f'https://raw.githubusercontent.com/jjmerits/Dashboard/main/01010{numofweek}{numofyear}final.HTML'
#with open(url) as f:
#t = requests.get(url,verify=False)
#st.markdown(t.text, unsafe_allow_html=True)
  
##########################


#########################



#st.set_page_config(layout='centered')
#st.write(df.head(5))

conn.close()
