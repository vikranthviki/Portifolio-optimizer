#!/usr/bin/env python
# coding: utf-8

# In[1]:


import yfinance as yf
import pandas as pd 
import numpy as np
from pypfopt import EfficientFrontier,objective_functions
from pypfopt import BlackLittermanModel
import plotly.express as px
import yahoo_fin
import yahoo_fin.stock_info as si
import math


# In[2]:


# for i in tickers:
#     print(i)
#     try: 
#         peg.append(i.info['pegRatio'])
#         inst_holder.append(i.info['heldPercentInstitutions'])
#         re_gr.append(i.info['revenueGrowth'])
#         cap.append(i.info['marketCap'])
#         beta.append(i.info['beta'])
#         industry.append(i.info['sector'])
#         name.append(i.info['shortName'])
#         reco.append(i.info['recommendationKey'])
#     except KeyError :
#         continue
          


# In[3]:


df_f=pd.read_csv('sp_final.csv')


# In[4]:


df_f.sort_values(['Industry','Market Cap'],ascending=False).head(20)


# In[5]:


sector=df_f['Industry'].unique()
company={}
for s in sector:
    company["df_{}".format(s)]=df_f[df_f['Industry']==s]


# In[6]:


beta_mean=[]
growth_mean=[]
marketcap_mean=[]
peg_mean=[]
for s in sector: 
    beta_mean.append(company['df_{}'.format(s)]['beta'].mean())
    growth_mean.append(company['df_{}'.format(s)]['Growth'].mean())
    marketcap_mean.append(company['df_{}'.format(s)]['Market Cap'].mean())
    peg_mean.append(company['df_{}'.format(s)]['PEG_ratio'].mean())


# In[7]:


ar=['beta','growth','market cap','peg']
k=np.vstack([beta_mean,growth_mean,marketcap_mean,peg_mean])
df_mean=pd.DataFrame(np.column_stack((ar,k)))
he= np.insert(sector, 0, 'sector', axis=0)


# In[8]:


df_mean.columns=he
df_mean.set_index(['sector'],inplace=True)
df_mean.transpose()


# In[9]:


s1=['Technology','Real Estate','Consumer Cyclical','Energy','Industrials']
s2=['Healthcare','Consumer Defensive','Financial Services','Basic Materials','Communication Services']


# In[10]:


port=[]
Name=[]
for i in range(len(df_f)):
    if df_f.iloc[i]['Industry'] in s1 and str(df_f.iloc[i]['PEG_ratio'])>df_mean[df_f.iloc[i]['Industry']]['peg'] and str(df_f.iloc[i]['Market Cap'])>df_mean[df_f.iloc[i]['Industry']]['market cap']:   
        port.append(df_f.iloc[i]['Ticker'])
        Name.append(df_f.iloc[i]['Name'])
    elif df_f.iloc[i]['Industry'] in s2 and str(df_f.iloc[i]['PEG_ratio'])<df_mean[df_f.iloc[i]['Industry']]['peg'] and str(df_f.iloc[i]['Growth'])>str(df_mean[df_f.iloc[i]['Industry']]['growth']): 
        port.append(df_f.iloc[i]['Ticker'])
        Name.append(df_f.iloc[i]['Name'])

cm=list(zip(port ,Name))


# In[11]:


price=yf.download(tickers='SPY',period='1y',interval='1d')['Adj Close']


# In[12]:


from pypfopt import black_litterman, risk_models
All_prices=yf.download(tickers=port[:20],period='6mo',interval='1d')['Adj Close']


# In[13]:





# In[14]:





# In[15]:


def com (se,d):
    n_c=math.ceil(100/d)
    e_n=math.ceil(n_c/len(se)) 
    f_port=[]
    f_name=[]
    k=df_f.groupby('Industry')
    for i in se:
        tem=k.get_group(i)
        if i in s1:
            tem.sort_values(['PEG_ratio','Market Cap'],ascending=False)
            f_port=np.concatenate((f_port,tem['Ticker'].values[0:e_n]),axis=0)
            f_name=np.concatenate((f_name,tem['Name'].values[0:e_n]),axis=0)
        if i in s2:
            tem.sort_values(['PEG_ratio','Market Cap'],ascending=True)
            f_port=np.concatenate((f_port,tem['Ticker'].values[0:e_n]),axis=0)
            f_name=np.concatenate((f_name,tem['Name'].values[0:e_n]),axis=0)

    return f_port,f_name        


# In[16]:


def black_allocation(b,viewdict,fport,ch):
    All_prices=yf.download(tickers=fport,period='6mo',interval='1d')['Adj Close']
    mcaps = {}
    S = risk_models.CovarianceShrinkage(All_prices).ledoit_wolf()
    delta = black_litterman.market_implied_risk_aversion(price)
    for t in fport:
        if t in port:
            mcaps[t] =float(df_f[df_f["Ticker"]==t]['Market Cap'])
        else:
            f=si.get_quote_table(t)['Market Cap']
            if f[len(f)-1]=='B':
                mcaps[t]=float((f[0:len(f)-1])*10**9)  
            if f[len(f)-1]=='T':
                mcaps[t]=float((f[0:len(f)-1])*10**12)
            if f[len(f)-1]=='M':  
                mcaps[t]=float((f[0:len(f)-1])*10**6)
    market_prior = black_litterman.market_implied_prior_returns(mcaps, delta, S)

    bl_confi= BlackLittermanModel(S,pi=market_prior,absolute_views=viewdict)
    bl_return = bl_confi.bl_returns()
    bl_return.name = 'Posterior'
    S_bl_confi = bl_confi.bl_cov()
    ef = EfficientFrontier(bl_return, S_bl_confi, weight_bounds=(0, b))
    #ef.add_objective(objective_functions.L2_reg, gamma=0.1)
    if ch=='ms':
        weights = ef.max_sharpe()
    if ch=='mv':
        weights = ef.min_volatility()
        weights = ef.clean_weights()
    wt_min_vola = pd.DataFrame([weights],columns=weights.keys()).T * 100
    wt_min_vola.index.names = ['Ticker']
    wt_min_vola.columns=['%alloted']
    fig = px.bar(wt_min_vola, x=wt_min_vola.index, y='%alloted', title='% alloted in each company')
    return fig,ef.portfolio_performance(verbose=False)


# In[17]:




# In[18]:




# In[ ]:





# In[ ]:




