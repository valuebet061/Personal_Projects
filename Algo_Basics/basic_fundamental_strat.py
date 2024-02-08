#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import bql
from scipy import math

bq = bql.Service()


# In[2]:


index = bq.univ.members(['SPX Index'])
name = bq.data.name()['VALUE']
cur_px = bq.data.px_last(fill = 'prev')['VALUE'] #[VALUE] turn
eps_est = bq.data.is_comp_eps_adjusted(fpt='A',fpo='2',est_source='BST')['VALUE']

req = bql.Request(index, [name, cur_px, eps_est]) #requesting from BQL
res = bq.execute(req) #response


pe_df = bql.combined_df(res) #combined DF of BBG requests
pe_df = pe_df.reset_index()


# In[3]:


pe_df.columns = ['Ticker', 'Co Name', 'CurPx', 'FY24 EPS'] #renaming columns
pe_df['FY24 P/E'] = pe_df['CurPx'] / pe_df['FY24 EPS'] #calculating P/E
pe_df['# of Shares to Buy'] = None #adding empty column for now
pe_df.sort_values('FY24 P/E', ascending = True, inplace = True) #sorting
pe_df = pe_df[pe_df['FY24 P/E'] > 0] #looking for positive
pe_df = pe_df[:50] #top 50
pe_df.reset_index(inplace = True)
pe_df.drop('index', axis=1, inplace = True)

pe_df


# In[4]:


#calcing number of shares to buy

def portfolio_input():
    global portfolio_size #global just affects every variable in the script with the same name
    portfolio_size = input("Enter the value of your porfolio: ")
    
    try:
        val = float(portfolio_size)
        val
    except ValueError:
        print("Try Again")
        portfolio_size = input("Enter the value of your porfolio: ")
        portfolio_input()


# In[ ]:


portfolio_input()


# In[ ]:


position_size = float(portfolio_size)/len(pe_df.index)
for row in pe_df.index:
    pe_df.loc[row, '# of Shares to Buy'] = math.floor(position_size/pe_df.loc[row, 'CurPx'])

pe_df


# In[ ]:




