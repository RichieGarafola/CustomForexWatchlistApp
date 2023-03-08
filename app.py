import yfinance as yf
import streamlit as st
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Define function to retrieve financial data for a given ticker and timeframe
def get_data(ticker, timeframe):
    data = yf.download(ticker, period=timeframe)
    return data

# Define function to create candlestick chart
def create_candlestick_chart(data, chart_color):
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                          open=data['Open'],
                                          high=data['High'],
                                          low=data['Low'],
                                          close=data['Close'],
                                          increasing_line_color=chart_color,
                                          decreasing_line_color=chart_color)])
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig

def create_heikin_ashi_chart(data, chart_color):
    # Create Heikin-Ashi dataframe
    df = data.copy()
    df['HA_Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
    df['HA_Open'] = df['Open']
    for i in range(1, len(df)):
        df.at[df.index[i], 'HA_Open'] = (df.at[df.index[i - 1], 'HA_Open'] + df.at[df.index[i - 1], 'HA_Close']) / 2
    df['HA_High'] = df[['HA_Open', 'HA_Close', 'High']].max(axis=1)
    df['HA_Low'] = df[['HA_Open', 'HA_Close', 'Low']].min(axis=1)
    
    # Create chart
    fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['HA_Open'], high=df['HA_High'], low=df['HA_Low'], close=df['HA_Close'], increasing_line_color=chart_color, decreasing_line_color='red')])
    fig.update_layout(title='Heikin-Ashi Chart', xaxis_rangeslider_visible=False)
    return fig

# Define function to create line chart
def create_line_chart(data, chart_color):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', line=dict(color=chart_color)))
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig

# Define function to display chart with the given type and color
def display_chart(data, chart_type, chart_color):
    if chart_type == "Candles":
        fig = create_candlestick_chart(data, chart_color)
    elif chart_type == "Heikin Ashi":
        fig = create_heikin_ashi_chart(data, chart_color)
    else:
        fig = create_line_chart(data, chart_color)
    st.plotly_chart(fig)

# Define the Streamlit app
def main():
    st.title("Customizable Watchlist Charts")
    st.sidebar.title("Settings")

    # Define the sidebar options for selecting symbols and timeframes
    symbols = ["audnzd=X", "audusd=X", "eurcad=X", "eurchf=X", "eurgbp=X", "eurusd=X", "gbpcad=X", "gbpchf=X", "gbpusd=X", "nzdusd=X", "usdcad=X", "usdchf=X"]
    selected_symbols = st.sidebar.multiselect("Select Symbols:", symbols, default=symbols[:4])
    timeframe = st.sidebar.selectbox("Select Timeframe:", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"])

    # Define the sidebar options for selecting chart settings
    chart_type = st.sidebar.selectbox("Select Chart Type:", ["Candles", "Heikin Ashi", "Line"])
    chart_color = st.sidebar.color_picker("Select Chart Color:", "#00ff00")
    show_price = st.sidebar.checkbox("Show Price")
    show_price_line = st.sidebar.checkbox("Show Price Line")
    labels_size = st.sidebar.slider("Select Labels Size:", min_value=10, max_value=30, value=15)
    text_size = st.sidebar.slider("Select Text Size:", min_value=10, max_value=30, value=15)
    gaps_between_charts = st.sidebar.slider("Select Gaps Between Charts:", min_value=0, max_value=100, value=10)

    # Define the main page content for displaying the selected symbols and their charts
    for symbol in selected_symbols:
        st.write(f"## {symbol} ({timeframe})")
        data = get_data(symbol, timeframe)
        display_chart(data, chart_type, chart_color)
        if show_price:
            st.write(f"Price: {data['Close'].iloc[-1]}")
        if show_price_line:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', line=dict(color=chart_color), name='Price'), secondary_y=True)
            fig.update_layout(yaxis_title="Candles", yaxis2_title="Price", xaxis_rangeslider_visible=False)
            st.plotly_chart(fig)
        st.write("---")
    
    # Define the global styles for the page
    st.markdown(f"""<style>
                .reportview-container .main .block-container{{
                    max-width: {1100}px;
                    padding-top: {gaps_between_charts}px;
                    padding-right: {gaps_between_charts}px;
                    padding-left: {gaps_between_charts}px;
                    padding-bottom: {gaps_between_charts}px;
                }}
                .reportview-container .main {{
                    color: {'white'};
                    background-color: {'black'};
                }}
                .reportview-container .sidebar {{
                    background-color: {'gray'};
                }}
                .css-17eq0hr {{
                    font-size: {labels_size}px;
                }}
                .css-hby737 {{
                    font-size: {text_size}px;
                }}
                </style>""", unsafe_allow_html=True)


if __name__ == '__main__':
    main()
    

                                                          