#!/usr/bin/env python
# coding: utf-8

# Momentum Strategy based on Moving Averages of Stocks
# 
# We'll use GLD ETF (Gold)

# In[56]:


import numpy as np
import pandas as pd
import pandas_datareader.data as pdr #.data helped fix
import yfinance as yf
yf.pdr_override() #fixing command
from datetime import datetime, timedelta #timedelta to get to T-5years
import matplotlib.pyplot as plt

#pip install yfinance --upgrade --no-cache-dir
#pip install fix-yahoo-finance


# In[57]:


today = datetime.today()
today_format = datetime(today.year, today.month, today.day)
five_years_ago = today - timedelta(days = 5 * 365)
fya_format = datetime(five_years_ago.year, five_years_ago.month, five_years_ago.day)

gld = pdr.get_data_yahoo('GLD', fya_format)
print("Prices from :" + str(five_years_ago.strftime("%Y-%m-%d")) + " to " + str(today.strftime("%Y-%m-%d")))
day = np.arange(1, len(gld) + 1) #generates an array that counts the length, starting at 1; we +1 because starts at 0
gld['Day'] = day
gld.drop(columns=['Adj Close', 'Volume'], inplace = True) #just taking out Adj. Close and Volume, some adjusted close is useful but not here
gld = gld[['Day', 'Open', 'High', 'Low', 'Close']]
gld.head()


# Add moving averages to the data frame

# In[58]:


#moving averages (slow and fast moving average) - get into trade when fast one crosses above the slow one + sell when fast one is below the short one.

gld['9-day'] = gld['Close'].rolling(9).mean().shift() #adding the 9-day/21-day + modifers that include: rolling X days average and average
gld['21-day'] = gld['Close'].rolling(21).mean().shift() #WE SHIFT 1 day BECAUSE THE DATA ASSUMES WE ALREADY HAVE THE CLOSE OF THE 20th day (which in practice we dont)


# In[69]:


#adding a "signal" column - when to long and short

gld['signal'] = np.where(gld['9-day'] > gld['21-day'], 1, 0) #IF statement in Excel 1 when true, 0 when false LONG
gld['signal'] = np.where(gld['9-day'] < gld['21-day'], -1, gld['signal']) #IF statement in Excel 1 when true, 0 when false SHORT - 
gld.dropna(inplace=True)
gld.head()


# In[70]:


#calcing returns, instant and system returns
gld['return'] = np.log(gld['Close']).diff() #logarithmic returns
gld['system_return'] = gld['signal'] * gld['return']
gld['entry'] = gld.signal.diff() #shows a +2 or -2 when we enter and exit, respectively
gld


# Plotting Trades on a time series

# In[72]:


plt.rcParams['figure.figsize'] = 12, 6 #sets a default side (12 width, 6 height in inches), rcParams stores configuration settings
plt.grid(True, alpha = .3)
plt.plot(gld.iloc[-252:]['Close'], label = 'GLD')
plt.plot(gld.iloc[-252:]['9-day'], label = '9-day')
plt.plot(gld.iloc[-252:]['21-day'], label = '21-day')
plt.plot(gld[-252:].loc[gld.entry == 2].index, gld[-252:]['9-day'][gld.entry == 2], '^', color = 'g', markersize = 12) #marker of when you buy based on entry column
plt.plot(gld[-252:].loc[gld.entry == -2].index, gld[-252:]['21-day'][gld.entry == -2], 'v', color = 'r', markersize = 12) #sell
plt.legend(loc=2);


# In[74]:


#testing vs. just buying and holding
plt.plot(np.exp(gld['return']).cumprod(), label='Buy/Hold') #shows cumulative return if you just bought and hold (adding up all log return)
plt.plot(np.exp(gld['system_return']).cumprod(), label='System') #if you used the strategy
plt.legend(loc=2)
plt.grid (True, alpha=.3)


# In[80]:


BnH_return = np.exp(gld['return']).cumprod()[-1] -1 #[-1] to take last number for total cum
print('Buy/Hold total return: ' + f"{BnH_return:.2f}%")

BnH_return = np.exp(gld['system_return']).cumprod()[-1] -1 #[-1] to take last number for total cum
print('System total return: ' + f"{BnH_return:.2f}%")


# In[ ]:




