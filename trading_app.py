import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(
    page_title='Stock Analysis',
    page_icon='📈',
    layout='wide'
)

st.title("Stock Analysis App:bar_chart:")
st.header("Charts don’t lie. We just read them better.")

img = Image.open("img.jpg")
img = img.resize((1000, 400))
st.image(img)

st.markdown("## What's we do??")
st.subheader(":one: Analyze stocks from companies across the market using historical price and trading data.")
st.subheader(":two: Visualize price trends, market movements, and key patterns through interactive charts.")
st.subheader(":three: Use forecasting models to estimate potential future price movements based on historical trends.")
st.subheader(":four: Turn complex market data into clear, easy-to-understand insights—all in one place.")

