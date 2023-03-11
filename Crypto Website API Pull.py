#!/usr/bin/env python
# coding: utf-8

# In[1]:


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'15',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '8c976e22-c5b1-401c-a9f4-517411c94924',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  #print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)


# In[2]:


type(data)


# In[3]:


import pandas as pd

# see all the columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# In[4]:


#normalize the data
df = pd.json_normalize(data['data'])
df['timestamp'] = pd.to_datetime('now')
df


# In[5]:


def api_runner():
    global df
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'15',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '8c976e22-c5b1-401c-a9f4-517411c94924',
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      #print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    
    df = pd.json_normalize(data['data'])
    df['timestamp'] = pd.to_datetime('now')
    df
    
    if not os.path.isfile(r'D:\Audi\projects\api\API.csv'):
        df.to_csv(r'D:\Audi\projects\api\API.csv', header='column_names')
    else:
        df.to_csv(r'D:\Audi\projects\api\API.csv', mode='a', header=False)


# In[6]:


import os
from time import time
from time import sleep

for i in range(333):
    api_runner()
    print("API RUNNER COMPLETED SUCCESSFULLY")
    sleep(60) #sleep for 1 minute
exit()


# In[7]:


df


# In[8]:


df72 = pd.read_csv(r'D:\Audi\projects\api\API.csv')
df72


# In[9]:


pd.set_option('display.float_format', lambda x: '%.5f' % x)


# In[10]:


df


# In[11]:


df3 = df.groupby('name', sort=False)[['quote.USD.percent_change_1h', 'quote.USD.percent_change_24h', 'quote.USD.percent_change_7d', 'quote.USD.percent_change_30d', 'quote.USD.percent_change_60d']].mean()
df3


# In[12]:


df4 = df3.stack()
df4


# In[13]:


type(df3)


# In[14]:


type(df4)


# In[15]:


df5 = df4.to_frame(name='values')
df5


# In[16]:


df5.count()


# In[17]:


index = pd.Index(range(75))

df6 = df5.reset_index()
df6


# In[18]:


df7 = df6.rename(columns={'level_1':'percent_change'})
df7


# In[19]:


df7['percent_change'] = df7['percent_change'].replace(['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d'],['1h','24h','7d','30d','60d','90d'])
df7


# In[20]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[21]:


sns.catplot(x='percent_change', y='values', hue='name', data=df7, kind='point')


# In[22]:


df8 = df[['name', 'quote.USD.price', 'timestamp']]
df8 = df8.query("name == 'Bitcoin'")
df8


# In[24]:


sns.set_theme(style="darkgrid")

sns.lineplot(x='timestamp', y='quote.USD.price', data = df8)


# In[ ]:





# In[ ]:




