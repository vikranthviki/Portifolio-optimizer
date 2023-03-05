import datetime
import time
import pandas as pd
import marshal,types
import streamlit as st
from port_opt import *
import yfinance as yf
from PIL import Image
se=['Technology','Real Estate','Consumer Cyclical','Energy','Industrials','Healthcare','Consumer Defensive','Financial Services','Basic Materials','Communication Services']
def main():
    st.set_page_config(page_title='Portifolio optimizer',page_icon="🕗", layout="centered", initial_sidebar_state="auto", menu_items=None)
    im ="C:/Users/vikranth/OneDrive/Desktop/programming/stock_project/Stock_bb.jpeg"
    #add_bg_from_local(im)    
    st.title("Portfolio otimizer with returns estimator")
    d = st.slider('Maximum percent allocation for each company', 1, 99)
    s=st.multiselect('sectors',se,  label_visibility="visible")
    c=com(s,d)
    co= pd.DataFrame(c[0])
    st.header('stocks alloted in portifolio')
    st.write(c[1])
    ch=st.selectbox('Do you want to add more stocks',['Yes','No'] ,index=1)
    if ch=='Yes':
        edited_co = st.experimental_data_editor(co, num_rows="dynamic")
    else:
        edited_co=co
    st.experimental_data_editor(co, num_rows="dynamic")   
    viewdict=dict(zip(c[0], [1]*len(c[0])))
    k=False
    if st.button('Click after giving views '):
        k=True
    st.experimental_data_editor( viewdict, num_rows="dynamic",disabled=k)
    if k==True:
        h=st.selectbox('Select max returns or min volatility', ['Max returns','Min voltality'],index=0)
        if h=='Max returns':
            re=black_allocation(d/10,viewdict,edited_co,'ms')
            st.write(re[0])
            st.write(str(re[1][0]*100)+'is expected annual returns')
            st.write(str(re[1][1]*100)+'is % of volatility')

        if h=='Min voltality':
            re=black_allocation(d/10,viewdict,edited_co,'mv')
            st.write(re[0])
            st.write(str(re[1][0]*100)+'is expected annual returns')
            st.write(str(re[1][1]*100)+'is % of volatility')          

    