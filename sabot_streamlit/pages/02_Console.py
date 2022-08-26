import os
from time import time
import pandas as pd
from pathlib import Path
import time
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import streamlit as st 

# from pytz import timezone
from dotenv import load_dotenv
load_dotenv()
import requests
import logging
from dateutil import tz
import sys   
file = Path(__file__). resolve()  
package_root_directory = file.parents [1]  
sys.path.append(str(package_root_directory))  
from sabot_data import get_latest_ohlcv,get_oldest_ohlcv,get_ohlcv_count,get_sabot_measurements,get_order_fulfillers

st.title("Console")


# configure sabot console logging
logFormatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s: %(message)s')
logger = logging.getLogger()

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)
logger.setLevel(logging.INFO)

if 'debug' in os.environ:
    if os.environ['debug'].strip().lower() == 'true':
        logger.setLevel(logging.DEBUG)


start_time = None
df = None
sources_df = None
def get_df():
    global df
    if df is None:
        results=get_sabot_measurements(os.environ['SABOT_CONTEXT'])
        df = pd.DataFrame(
                results['values'],
                columns=results['columns'])
        df['local time'] = df['time'].apply(to_local_time)
        df['decision_label'] = df['decision'].astype(str).apply(translate_decision)
        df.set_index('time',inplace=True)
        df = df[['local time', 'decision_label', 'decision', 'portfolio_value',f"wallet_{os.environ['SABOT_STABLECOIN']}",f"wallet_{os.environ['SABOT_TARGET_COIN']}",f"comp_{os.environ['SABOT_TARGET_COIN']}",'reason', 'gas', 'effective_pct_fee']]
    logger.debug(df)
    return df

def get_uptime():
    global start_time
    if start_time is None:
        start_time = get_df().index.min()
    end = int(datetime.now().timestamp()*1000)
    return f"{(float(end - start_time)/float(1000)/float(60)/float(60)):.2f} hours"

def get_decisions():
    return get_df().shape[0]

def get_record_count(coin):
    count = get_ohlcv_count(coin)
    return count

def get_oldest_date(coin):
    oldest = get_oldest_ohlcv(coin)[coin][0]['time'] / 1000
    dt = datetime.fromtimestamp(oldest,tz=timezone.utc)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def get_latest_date(coin):
    latest = get_latest_ohlcv(coin)[coin][0]['time'] / 1000
    dt = datetime.fromtimestamp(latest,tz=timezone.utc)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def to_local_time(row):
    dt = datetime.fromtimestamp(int(row/1000),tz=timezone.utc)
    new_dt =  dt.astimezone(tz.tzlocal())
    logger.debug(f"{row}: {dt} -> {new_dt}")
    return new_dt.strftime('%Y-%m-%d %H:%M:%S')

def get_portfolio_value():
    return get_df().iloc[-1,:]['portfolio_value']

def get_portfolio_change():
    current_value = get_portfolio_value()
    original_value = get_df().iloc[0,:]['portfolio_value']
    return current_value - original_value

def get_current_balance(coin):
    return get_df().iloc[-1,:][f'wallet_{coin}']

def translate_decision(y):
    if y=='1':
        return 'buy'
    if y=='-1':
        return 'sell'
    return 'hold'

def get_decisions_df():
    decisions_df = None
    decisions_df = get_df()
    decisions_df = df.reset_index(level=0, drop=True).reset_index()
    decisions_df = decisions_df[['local time', 'decision_label','reason','gas','effective_pct_fee',f"comp_{os.environ['SABOT_TARGET_COIN']}"]]
    decisions_df.rename(columns={"local time":"time", "effective_pct_fee": "% fee", "decision_label":"decision",f"comp_{os.environ['SABOT_TARGET_COIN']}":"sUSD"},inplace=True)
    return decisions_df

def get_order_fulfillers_df():
    global sources_df
    if sources_df is None:
        results=get_order_fulfillers(os.environ['SABOT_CONTEXT'])
        sources_df = pd.DataFrame(
                results['values'],
                columns=results['columns'])
        sources_df.set_index('time',inplace=True)
    return sources_df, sources_df['order_source'].value_counts()

def get_last_update_time():
    return get_df().index[-1]


st.set_page_config(layout="wide")

with st.container():
    logo_col, title_col = st.columns([5,95])
    with logo_col:
        st.image(os.environ['SABOT_LOGO'])
    with title_col:
        st.markdown('<div><span style="font-size: 56px; font-weight: 700; position: relative; top: -26px;">SaBot</span></div>', 
        unsafe_allow_html=True)

done = False
with st.empty():
    while not done:
        update = {
            'time': get_last_update_time(),
            'uptime':get_uptime(),
            'decisions':get_decisions(),
            'value':get_portfolio_value(),
            'delta':float(get_portfolio_change()),
            'wallet_USDT':get_current_balance("USDT"),
            'wallet_SUSD':get_current_balance("SUSD-USDT")
        }
        with st.container():
            with st.container():
                sabot_col, portfolio_col, wallet_usdt_col, wallet_susd_col = st.columns([25,25,25,25])
                with sabot_col:
                    st.header(f"SaBot - {os.environ['SABOT_CONTEXT']}")
                    st.metric("Up Time", update['uptime'])
                    st.metric("Decisions", update['decisions'])
                with portfolio_col:
                    st.header('Portfolio')
                    st.metric("Value", update['value'], update['delta'])
                with wallet_usdt_col:
                    st.header('Wallet USDT')
                    st.metric("Balance", update['wallet_USDT'])
                with wallet_susd_col:
                    st.header('Wallet SUSD')
                    st.metric("Balance", update['wallet_SUSD'])
            st.markdown('---')
            results_tab, sources_tab = st.tabs(["Results", "Sources"])
            with results_tab:
                with st.container():
                    decisions_col, plot_col,left_data_col, right_data_col = st.columns([32,38,15,15])
                    with decisions_col:
                        st.header('Decisions')
                        st.write(get_decisions_df())
                    with plot_col:
                        st.header(f"Sabot Portfolio Return")
                        st.line_chart(get_df()[['portfolio_value',f"comp_{os.environ['SABOT_TARGET_COIN']}"]])
                    with left_data_col:
                        with st.container():
                            st.header('BTC')
                            st.metric("Hourly Data Points", get_record_count("BTC"))
                            st.metric("From", get_oldest_date("BTC"))
                            st.metric("Lastest", get_latest_date("BTC"))
                        with st.container():
                            st.header('USDT')
                            st.metric("Hourly Data Points", get_record_count("USDT"))
                            st.metric("From", get_oldest_date("USDT"))
                            st.metric("Lastest", get_latest_date("USDT"))
                    with right_data_col:
                        with st.container():
                            st.header('ETH')
                            st.metric("Hourly Data Points", get_record_count("ETH"))
                            st.metric("From", get_oldest_date("ETH"))
                            st.metric("Lastest", get_latest_date("ETH"))
                        with st.container():
                            st.header('SUSD-USDT')
                            st.metric("Hourly Data Points", get_record_count("SUSD-USDT"))
                            st.metric("From", get_oldest_date("SUSD-USDT"))
                            st.metric("Lastest", get_latest_date("SUSD-USDT"))
            with sources_tab:
                with st.container():
                    sources_df,sources_counts_df = get_order_fulfillers_df()
                    sources_col, sources_hist_col = st.columns([50,50])
                    with sources_col:
                        st.header('Sources')
                        st.write(sources_df)
                    with sources_hist_col:
                        st.bar_chart(sources_counts_df)

        time.sleep(3)