import streamlit as st
import plotly.graph_objs as go
from bsedata.bse import BSE
import time

bse = BSE(update_codes=True)

st.set_page_config(page_title="Live Sensex Dashboard", layout="wide")
st.title("📈 Live Sensex Dashboard")

def get_sensex_data():
    data = bse.getIndexQuote('SENSEX')
    return float(data['Current Value'])

placeholder = st.empty()
chart = st.empty()

# Store values using Streamlit's session state
if 'x_vals' not in st.session_state:
    st.session_state.x_vals = []
    st.session_state.y_vals = []

# Create stop button
stop = st.button("Stop Updates")

if not stop:
    sensex_val = get_sensex_data()
    st.session_state.x_vals.append(time.strftime("%H:%M:%S"))
    st.session_state.y_vals.append(sensex_val)

    placeholder.metric("📍 Current Sensex", f"{sensex_val:,.2f}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=st.session_state.x_vals, y=st.session_state.y_vals, mode='lines+markers'))
    fig.update_layout(title="Live Sensex Trend", xaxis_title="Time", yaxis_title="Value")
    chart.plotly_chart(fig, use_container_width=True)

    # Rerun the script every 10 seconds
    time.sleep(10)
    st.experimental_rerun()
