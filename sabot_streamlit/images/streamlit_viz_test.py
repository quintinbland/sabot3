# Imports
import pandas as pd
import streamlit as st
import numpy as np

# Page setting
st.set_page_config(layout="centered", page_title="Sabot") #, initial_sidebar_state="auto")

with open('style2.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("CLOG Price Chart (CLOG/USD)")

# Row A
a1, a2, a3, a4 = st.columns(4)
a1.metric("CLOG Value", "10.00$")
a2.metric("Amount of CLOGS", "1,000")
a3.metric("Portfolio Total Value", "5,322$")
a4.metric("Portfolio Return", "11.00%")


tab1, tab2, tab3 = st.tabs(["24hrs", "7days", "30days"])

with st.container():
    st.write("This is inside the container")

    with tab1:
        st.header("Historical Account Value")

        # You can call any Streamlit command, including custom components:
        st.area_chart(np.random.randn(50, 1))

    with tab2:
        st.header("Historical Account Value")
        # You can call any Streamlit command, including custom components:
        st.area_chart(np.random.randn(100, 1))

    with tab3:
        st.header("Historical Account Value")
        # You can call any Streamlit command, including custom components:
        st.area_chart(np.random.randn(150, 1))


data = pd.read_csv("./data/sabot_events.log")

chart_data = pd.DataFrame(data, columns=["time", "sellTokenAmount"])
chart_data_clean = chart_data.dropna()
st.area_chart(chart_data_clean)

# st.write(df_data)