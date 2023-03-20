#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import libraries
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from matplotlib.pyplot import figure

get_ipython().run_line_magic('matplotlib', 'inline')
matplotlib.rcParams['figure.figsize'] = (12, 8) #adjust the configuration of the plots we will create

#read in the data
df = pd.read_csv('D:\Audi\projects\movies.csv')


# In[2]:


#look at the data
df.head()


# In[3]:


#check if there is any missing data
for col in df.columns:
    pct_missing = np.mean(df[col].isnull())
    print('{} - {}%'.format(col, pct_missing))


# In[4]:


#data types for our columns
df.dtypes


# In[5]:


#change data type of columns
df['budget'] = pd.to_numeric(df['budget'], errors='coerce').fillna(0).astype(int)
df['gross'] = pd.to_numeric(df['gross'], errors='coerce').fillna(0).astype(int)


# In[6]:


df = df.dropna(how='any', axis=0)


# In[7]:


#create correct year column
df['yearcorrect'] = df['released'].str.extract(pat ='([0-9]{4})').astype(int)


# In[8]:


df.sort_values(by=['gross'], inplace=False, ascending=False)


# In[9]:


pd.set_option('display.max_rows', None)


# In[10]:


#budget vs gross earnings using pyplot
plt.scatter(x=df['budget'], y=df['gross'])
plt.title("Budget vs Gross Earnings")
plt.xlabel("Budget for film")
plt.ylabel("Gross earnings")
plt.show()


# In[11]:


#budget vs gross earnings using seaborn
sns.regplot(x='budget', y='gross', data=df, scatter_kws={"color":"red"},line_kws={"color":"blue"})


# In[12]:


#Looking at correlation
df.corr()


# In[13]:


#high correlation between budget and gross


# In[14]:


correlation_matrix = df.corr()
sns.heatmap(correlation_matrix, annot=True)
plt.title('Correlation Matrix for Numeric Features')
plt.xlabel('Movie Features')
plt.ylabel('Movie Features')
plt.show()


# In[15]:


df_numerized = df

for col_name in df_numerized.columns:
    if (df_numerized[col_name].dtype =='object'):
        df_numerized[col_name] = df_numerized[col_name].astype('category')
        df_numerized[col_name] = df_numerized[col_name].cat.codes
        
df_numerized.head()


# In[16]:


correlation_matrix = df_numerized.corr()
sns.heatmap(correlation_matrix, annot=True)
plt.title('Correlation Matrix for Numeric Features')
plt.xlabel('Movie Features')
plt.ylabel('Movie Features')
plt.show()


# In[22]:


correlation_mat = df_numerized.corr()
corr_pairs = correlation_mat.unstack()
corr_pairs


# In[23]:


sorted_pairs = corr_pairs.sort_values()


# In[24]:


high_corr = sorted_pairs[(sorted_pairs) > 0.5]
high_corr


# In[25]:


#votes and budget have the highest correlation to gross earnings
#company has low correlation


# In[ ]:




