import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from utils.model_training import get_data,get_rolling_mean,get_differencing_order,scaling,evaluate_model,get_forecast,inverse_scaling
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Stock Analysis",
    page_icon="📒",
    layout='wide'
)

st.title("Stock Close Price Prediciton")
col1,col2,col3=st.columns(3)

with col1:
    ticker=st.text_input("Choose Company Ticker: ","AAPL")

st.subheader("Predicitng next 30 days close price for: "+ticker)

close_price=get_data(ticker)
rolling_price=get_rolling_mean(close_price)

difference_order=get_differencing_order(rolling_price)
scaled_data,scaler=scaling(rolling_price)
rmse=evaluate_model(scaled_data,difference_order)

st.write("**Model RMSE Score:** ",rmse)

forecast=get_forecast(scaled_data,difference_order)

forecast['Close']=inverse_scaling(scaler,forecast['Close'])
st.write("**Next 30 Days Forecast:**")

fig_tail = forecast.sort_index(ascending=False)
st.dataframe(fig_tail)

st.write("Graphically:")

fig, ax = plt.subplots()
ax.plot(fig_tail.index, fig_tail["Close"])
ax.tick_params(axis='x', labelrotation=90)

st.pyplot(fig)