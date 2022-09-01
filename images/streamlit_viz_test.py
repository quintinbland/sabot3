# Imports
import pandas as pd
import streamlit as st
import numpy as np
import datetime

# Page setting.
st.set_page_config(layout="centered", page_title="Sabot") #, initial_sidebar_state="auto")

# CSS Settings.
with open('style2.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Page Title.
st.title("CLOG Price Chart (CLOG/USD)")

# Load Sabot Event Logs and filter Swapped type.
df = pd.read_csv("./data/sabot_events.log")
df = df[df["type"] == "Swapped"] 

# Slice out the first 20 rows of the dataframe and filter the targeted column.
df_data = pd.DataFrame(df[20:], columns=["time", "type", "utilityTokenTotalSupply", "balanceOfBaseToken", "balanceOfTargetToken"])

# Add a CLOG price value to a new colmn after operation.
df_data["CLOG_Price"] = (( df_data["balanceOfBaseToken"] + df_data["balanceOfTargetToken"] ) / df_data["utilityTokenTotalSupply"]) * 1000000000000

# Clean up dataframe by dropping empty records.
df_data_clean = df_data[["time", "CLOG_Price"]].dropna()

# Reset index.
# df_data_clean.reset_index(inplace = True)
df_data_clean["time"] = pd.to_datetime(df_data_clean["time"], unit = "s")
df_data_clean = df_data_clean.set_index(["time"])

# Define metric variables.
clog_value = df_data_clean["CLOG_Price"].iat[-1]
# clog_amount = df_data_clean[-1, df_data_clean.get_loc("utilityTokenTotalSupply")]
# portfolio_value = df_data_clean["balanceOfBaseToken"].iat[-1] + df_data_clean["balanceOfTargetToken"].iat[-1]

# Metric Row
a1, a2, a3 = st.columns(3)
a1.metric("CLOG Value", f"{clog_value:.2f} $")
a2.metric("Amount of CLOGS", "1,000") # clog_amount )
a3.metric("Portfolio Total Value", "5,460$") # f"{portfolio_value} $")

# Tabs for Chart
tab1, tab2, tab3 = st.tabs(["24hrs", "7days", "30days"])

with st.container():

    with tab1:
        st.header("Historical Account Value")
        st.area_chart(df_data_clean)

    with tab2:
        st.header("Historical Account Value")
        st.area_chart(np.random.randn(100, 1))

    with tab3:
        st.header("Historical Account Value")
        st.area_chart(np.random.randn(150, 1))
