#!/usr/bin/env python
# coding: utf-8

#     Mean Reversion Trading Algorithm; assumes back to an average after too far away

# In[2]:


import numpy as np
import pandas as pd
import pandas_datareader.data as pdr #.data helped fix
import yfinance as yf
yf.pdr_override() #fixing command
from datetime import datetime, timedelta #timedelta to get to T-5years
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sb
sb.set()


# In[3]:


today = datetime.today()
today_format = datetime(today.year, today.month, today.day)
five_years_ago = today - timedelta(days = 5 * 365)
fya_format = datetime(five_years_ago.year, five_years_ago.month, five_years_ago.day)

gld = pdr.get_data_yahoo('GLD', fya_format)
print("Prices from :" + str(five_years_ago.strftime("%Y-%m-%d")) + " to " + str(today.strftime("%Y-%m-%d")))
day = np.arange(1, len(gld) + 1) #generates an array that counts the length, starting at 1; we +1 because starts at 0
gld['Day'] = day
gld.drop(columns=['Adj Close', 'Volume'], inplace = True) #just taking out Adj. Close and Volume, some adjusted close is useful but not here
gld = gld[['Close']]
gld.head()


# In[7]:


ma = 21 #setting variable for moving average
gld['returns'] = np.log(gld['Close']).diff()
gld['ma'] = gld['Close'].rolling(ma).mean() #rolling average based on ma; this is the average you are looking at
gld['ratio'] = gld['Close'] / gld['ma']

gld['ratio'].describe()


# In[8]:


#defining what is "too far away from mean "1""

percentiles = [5, 10, 50, 90, 95]
p = np.percentile(gld['ratio'].dropna(), percentiles)


# In[9]:


gld['ratio'].dropna().plot(legend = True)
#plotting lines for percetiles
plt.axhline(p[0], c= (.5,.5,.5), ls='--') #[0] = 5th percentile
plt.axhline(p[2], c= (.5,.5,.5), ls='--') #[2] = 50th
plt.axhline(p[-1], c= (.5,.5,.5), ls='--') #[-1] = the last in the 


# In[20]:


#Building Algorithm;

#defining where we go short; (95%)
short = p[-1]
#where we go long (5th percentile)
long = p[0]
gld['position'] = np.where(gld.ratio > short, -1, np.nan)
gld['position'] = np.where(gld.ratio < long, 1, gld['position'])
gld['position'] = gld['position'].ffill()


# In[21]:


gld.position.dropna().plot()


# In[22]:


#strategy return vs. Buy/Hold Returns

gld['strat_return'] = gld['returns'] * gld['position'].shift()


# In[23]:


#plotting the returns
plt.plot(np.exp(gld['returns'].dropna()).cumprod(), label ='Buy/Hold')
plt.plot(np.exp(gld['strat_return'].dropna()).cumprod(), label='Strategy');
plt.legend();

print(gld['strat_return'])


# In[24]:


#finidng absolute return number
print(np.exp(gld['returns'].dropna()).cumprod()[-1] -1)
print(np.exp(gld['strat_return'].dropna()).cumprod()[-1] - 1)


# In[ ]:




