import streamlit as st
import pandas as pd
import yfinance as yf
import ta
import matplotlib.pyplot as plt
import datetime
import mplfinance as mpf

st.set_page_config(
    page_title="Stock Analysis",
    page_icon="📒",
    layout='wide'
)

st.title("Stock Analysis")

col1,col2,col3=st.columns(3)

today=datetime.date.today()

with col1:
    ticker=st.text_input("Choose Company Ticker: ","AAPL")

with col2:
    start_date=st.date_input("Choose Start Date", datetime.date(today.year-1,today.month,today.day))

with col3:
    end_date=st.date_input("Choose End Date",datetime.date(today.year,today.month,today.day))

st.subheader(f"Ticker You Choose: {ticker}")

stock=yf.Ticker(ticker)

st.write(stock.info['longBusinessSummary'])
st.write("**Sector**",stock.info['sector'])
st.write("**Full Time Employees**",stock.info['fullTimeEmployees'])
st.write("**Website**",stock.info['website'])


col1,col2=st.columns(2)

with col1:
    df=pd.DataFrame(index=['Market Cap','Beta','EPS','PE Ratio','Last Fiscal Year End'])
    df['']= [stock.info['marketCap'],stock.info['beta'],stock.info['trailingEps'],stock.info['trailingPE'],stock.info['lastFiscalYearEnd']]
    st.dataframe(df)

with col2:
    df=pd.DataFrame(index=['Quick Ratio','Revenue per share','Profit Margin','Debt to Equity','Return to Equity'])
    df['']= [stock.info['quickRatio'],stock.info['revenuePerShare'],stock.info['profitMargins'],stock.info['debtToEquity'],stock.info['returnOnEquity']]
    st.dataframe(df)



data=yf.download(ticker,start=start_date,end=end_date)

daily_change=data['Close'][ticker].iloc[-1]-data['Close'][ticker].iloc[-2]
col1.metric("Daily Change",str(round(data['Close'][ticker].iloc[-1],2)),str(round(daily_change,2)))


last_10_df=data.tail(10).sort_index(ascending=False)
st.write("#### Last 10 days Data")
st.dataframe(last_10_df)

st.write("### Choose the timeline: ")
col1,col2,col3,col4,col5,col6=st.columns(6)

# Store selected timeline
if 'num_period' not in st.session_state:
    st.session_state.num_period = ''

with col1:
    if st.button('10D'):
        st.session_state.num_period = '10d'
        
with col2:
    if st.button('1M'):
        st.session_state.num_period = '1mo'

with col3:
    if st.button('3M'):
        st.session_state.num_period = '3mo'

with col4:
    if st.button('6M'):
        st.session_state.num_period = '6mo'

with col5:
    if st.button('1Y'):
        st.session_state.num_period = '1y'

with col6:
    if st.button('2Y'):
        st.session_state.num_period = '2y'
        

num_period = st.session_state.num_period

col1,col2,col3=st.columns([1,1,4])

with col1:
    selected_option=st.selectbox('',('Candle','Line'))
with col2:
    if selected_option=='Line':
        selected_type=st.selectbox('',('Moving Average','Normal'))

ticker_=yf.Ticker(ticker)

if num_period == '':
    plot_data = ticker_.history(period='max')
else:
    plot_data = ticker_.history(period=num_period)

if plot_data.empty:

    st.error("No data available for the selected timeline.")

else:
    #candle chart
    if selected_option=='Candle':
        plot_data.index = pd.to_datetime(plot_data.index)
        mc = mpf.make_marketcolors(
            up='green',
            down='red',
            edge='inherit',
            wick='inherit'
        )

        style = mpf.make_mpf_style(
            marketcolors=mc,
            facecolor='#1e1e1e',
            figcolor='#1e1e1e',
            gridcolor='#444444',
            gridstyle='-',
            rc={
                'axes.labelcolor': 'white',
                'xtick.color': 'white',
                'ytick.color': 'white',
                'text.color': 'white'
                }
        )

        fig, axes = mpf.plot(
            plot_data,
            type='candle',
            style=style,
            returnfig=True
        )
        

        st.pyplot(fig)

    #line chart
    else:
        fig, ax = plt.subplots()

        fig.patch.set_facecolor('#1e1e1e')
        ax.set_facecolor('#1e1e1e')

        # Normal Line
        if selected_type == 'Normal':

            ax.plot(plot_data['Close'])

        # Moving Average
        else:

            ax.plot(plot_data['Close'], label='Close')

            moving_average = plot_data['Close'].rolling(20).mean()

            ax.plot(moving_average, label='20 Day Moving Average')

            ax.legend()

        ax.tick_params(colors='white')

        st.pyplot(fig)