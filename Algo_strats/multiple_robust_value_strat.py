#!/usr/bin/env python
# coding: utf-8

# P/E Ratio
# P/B Ratio
# EV/Sales
# EV/EBIT
# EV/EBITDA
# 
# rv = robust value

# In[ ]:


import numpy as np #The Numpy numerical computing library
import pandas as pd #The Pandas data science library
import requests #The requests library for HTTP requests in Python 
import math #The Python math module
from scipy import stats #The SciPy stats module
import bql

bq = bql.Service()


# In[ ]:


def fiscal_year_input():
    global fiscal_year
    fiscal_year = input("Enter FY: ")
    
    try:
        val = float(fiscal_year)
        val
    except ValueError:
        print("Try Again")
        fiscal_year_input()


# In[ ]:


fiscal_year_input()

pd.set_option('display.float_format', lambda x: f'{x:,.1f}') #switching from scientific to numerical, using f string

index = bq.univ.members(['SPX Index'])
name = bq.data.name()['VALUE']
cur_px = bq.data.px_last(fill = 'prev')['VALUE'] #[VALUE] turn


#Enterprise Value
mkt_cap = bq.data.cur_mkt_cap()['VALUE']
net_debt = bq.data.net_debt().znav()['VALUE']
minorities = bq.data.minority_noncontrolling_interest().znav()['VALUE']
pension_reserve = bq.data.bs_pension_rsrv().znav()['VALUE']
pref_equity = bq.data.bs_pfd_eqy().znav()['VALUE']
associates = bq.data.bs_invest_in_assoc_co().znav()['VALUE']
ent_val = (mkt_cap + net_debt + minorities + pref_equity - associates)

rev_est = bq.data.is_comp_sales(fpt='A', fpr=fiscal_year, est_source='BST')['VALUE']
ebit_est = bq.data.is_comparable_ebit(fpt='A',fpr=fiscal_year,est_source='BST')['VALUE']
ebitda_est = bq.data.is_comparable_ebitda(fpt = 'a', fpr = fiscal_year, est_source='BST').avail(bq.data.ebitda(fpt = 'a', fpr = fiscal_year, est_source='BST'), bq.data.is_comparable_ebit(fpt = 'a', fpr = fiscal_year, est_source='BST') + bq.data.cf_depr_amort(fpt = 'a', fpr = fiscal_year, est_source='BST')
)['Value']
eps_est = bq.data.is_comp_eps_adjusted(fpt='A',fpr=fiscal_year,est_source='BST')['VALUE']
fcf_est = bq.data.headline_FCF(fpt='A',fpr=fiscal_year,est_source='BST')['VALUE']

req = bql.Request(index, [name, cur_px, mkt_cap, ent_val, rev_est, ebit_est, ebitda_est, fcf_est, eps_est]) #requesting each metric from BQL
res = bq.execute(req) #response


final_df = bql.combined_df(res) #combined DF of BBG requests
final_df = final_df.reset_index()

cols_to_mns = final_df.columns[3:9]
final_df[cols_to_mns] = final_df[cols_to_mns]/1000000 #to show in mns just from EV to FCF Est

print('For Fiscal Year ' + fiscal_year)

final_df.columns = ['Ticker', 'Co Name', 'CurPx', 'Mkt Cap (mns)', 'EV (mns)', 'Rev (mns)', 'EBIT (mns)', 'EBITDA (mns)', 'FCF (mns)', 'EPS (mns)']
final_df


# In[ ]:


#creating Valuation Multiples

multiples = { #calculating the multiple
    "EV_rev": final_df["EV (mns)"] / final_df["Rev (mns)"],
    "EV_EBIT": final_df["EV (mns)"] / final_df["EBIT (mns)"],
    "EV_EBITDA": final_df["EV (mns)"] / final_df["EBITDA (mns)"],
    "P_FCF": final_df["Mkt Cap (mns)"] / final_df["FCF (mns)"],
    "P_E": final_df["CurPx"] / final_df["EPS (mns)"],
}


rv_columns = [
    'Ticker',
    'Company Name',
    'CurPx',
    'MktCap (mns)',
    'Ent Value (mns)',
    'No of Shs. to Buy',
    'EV/Rev',
    'EV/Rev Percentile',
    'EV/EBITDA',
    'EV/EBITDA Percentile',
    'P/E',
    'P/E Percentile',
    'P/FCF',
    'P/FCF Percentile',
    'RV Score',
]

rv_dataframe = pd.DataFrame(columns = rv_columns)
rv_dataframe

rv_dataframe = pd.DataFrame({ #putting new multiples into the dataframe
    "Ticker": final_df["Ticker"],
    "CurPx": 'N/A',
    "Company Name": final_df["Co Name"],  # Access values from final_df
    "CurPx": final_df["CurPx"],
    "MktCap (mns)": final_df["Mkt Cap (mns)"],
    "Ent Value (mns)": final_df["EV (mns)"],
    'No of Shs. to Buy': 'N/A',
    'EV/Rev': final_df["EV (mns)"] / final_df["Rev (mns)"],
    'EV/Rev Percentile': 'N/A',
    'EV/EBITDA': final_df["EV (mns)"] / final_df["EBITDA (mns)"],
    'EV/EBITDA Percentile': 'N/A',
    'P/E': final_df["CurPx"] / final_df["EPS (mns)"],
    'P/E Percentile': 'N/A',
    'P/FCF': final_df["Mkt Cap (mns)"] / final_df["FCF (mns)"],
    'P/FCF Percentile': 'N/A',
    'RV Score': 'N/A' 
})

rv_dataframe
# print('For Fiscal Year ' + fiscal_year)
# multiples_df.columns = ['Ticker', 'Co Name', 'CurPx', 'Mkt Cap (mns)', 'EV (mns)', 'EV/Revs', 'EV/EBIT', 'EV/EBITDA', 'P/FCF', 'P/E']

# multiples_df


# In[ ]:


len(rv_dataframe[rv_dataframe.isnull().any(axis=1)]) #Data with errors


# We can either (1) delete the data or (2) Fill the data
# 
# For now, just taking the average of all other rows

# In[ ]:


for column in ['EV/Rev', 'EV/EBITDA', 'P/E', 'P/FCF']:
    rv_dataframe[column].fillna(rv_dataframe[column].mean(), inplace = True) #fililng na in each column with mean of the values in the column- inplace is true because 


# In[ ]:


len(rv_dataframe[rv_dataframe.isnull().any(axis=1)]) #0 is a good answer


# Calculating Value Percentiles

# In[ ]:


metrics = {
    'EV/Rev': 'EV/Rev Percentile',
    'EV/EBITDA': 'EV/EBITDA Percentile',
    'P/E': 'P/E Percentile',
    'P/FCF': 'P/FCF Percentile',
}

for metric in metrics.keys(): #going through every key in the metrics dictionary
    for row in rv_dataframe.index: #now going through every row
        rv_dataframe.loc[row, metrics[metric]] = stats.percentileofscore(rv_dataframe[metric], rv_dataframe.loc[row, metric]) #(entire column, value of row column)

        
rv_dataframe


# In[ ]:


#Calculating RV = mean of the 4 percentile scores

from statistics import mean

for row in rv_dataframe.index:
    value_percentiles = []
    for metric in metrics.keys():
        value_percentiles.append(rv_dataframe.loc[row, metrics[metric]]) #putting in percentiles from metrics into empty value_percentile
    rv_dataframe.loc[row, 'RV Score'] = mean(value_percentiles) #mean of percentiles into RV_score

rv_dataframe


# In[ ]:


#taking 50 best stocks

rv_dataframe.sort_values('RV Score', ascending = True, inplace = True) #want lowest

rv_dataframe = rv_dataframe[:50]
rv_dataframe.reset_index(drop = True, inplace = False)
rv_dataframe


# In[ ]:


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
        
portfolio_input()


# In[ ]:


position_size = float(portfolio_size)/len(rv_dataframe.index)
for row in rv_dataframe.index:
    rv_dataframe.loc[row, 'No of Shs. to Buy'] = math.floor(position_size/rv_dataframe.loc[row, 'CurPx']) #math floor rounds to nearest integer

print('For Fiscal Year ' + fiscal_year)
print('Portfolio Size ' + portfolio_size)
rv_dataframe


# In[ ]:





# In[ ]:





# In[ ]:




