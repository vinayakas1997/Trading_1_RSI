import numpy as np 
import pandas_ta as ta
import pandas as pd 
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
try:
    df = pd.read_csv("EURUSD_2003-05-05_2024-10-16_4_hour.csv")
except Exception as e:
    print(e)


print(df.columns)
columns=['Date','Time', 'Open', 'High', 'Low', 'Close', 'Volume']
df=df[columns]
df = df[df['Volume'] != 0]  # remove rows with volume = 0
df.reset_index(drop=True, inplace=True)
#print(len(df))

df['RSI'] = ta.rsi(df['Close'], length=14)
print(df.head(20))

def pivotid(df1,l,n1,n2):
    if l-n1<0 or l+n2>len(df1):
        return 0
    pividlow=1
    pividhigh=1
    for i in range(l-n1,l+n2+1):
        if(df1.Low[l]>df1.Low[i]):
            pividlow=0
        if(df1.High[l]<df1.High[i]):
            pividhigh=0
    if pividlow and pividhigh:
        return 3 
    if pividlow:
        return 1 
    if pividhigh:
        return 2
    else:
        return 0

def rsipivotid(df1,l,n1,n2):
    if l-n1<0 or l+n2>len(df1):
        return 0
    pividlow=1
    pividhigh=1
    for i in range(l-n1,l+n2+1):
        if(df1.Low[l]>df1.Low[i]):
            pividlow=0
        if(df1.High[l]<df1.High[i]):
            pividhigh=0
    if pividlow and pividhigh:
        return 3 
    if pividlow:
        return 1 
    if pividhigh:
        return 2
    else:
        return 0
df['pivot']= df.apply(lambda x: pivotid(df,x.name,5,5),axis=1)
df['RSIpivot']= df.apply(lambda x: rsipivotid(df,x.name,5,5),axis=1)


def pointpos(x):
    if x['pivot'] == 1:
        return x['Low']-1e-3
    if x['pivot'] == 2:
        return x['High']+1e-3
    if x['pivot'] == 3:
        return np.nan

def rsipointpos(x):
    if x['RSIpivot'] == 1:
        return x['Low']-1e-3
    if x['RSIpivot'] == 2:
        return x['High']+1e-3
    if x['RSIpivot'] == 3:
        return np.nan
df['pointpos']= df.apply(lambda row: pointpos(row),axis=1)
df['RSIpointpos']=df.apply(lambda row: rsipointpos(row),axis=1)

fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Candlestick'),
                      go.Scatter(x=df.index, y=df['RSI'], mode='lines', name='RSI', yaxis='y2'),
                      go.Scatter(x=df.index, y=df['pointpos'], mode='markers', name='Pivot', marker=dict(color='red', size=10, symbol='triangle-down')),
                      go.Scatter(x=df.index, y=df['RSIpointpos'], mode='markers', name='RSI Pivot', marker=dict(color='green', size=10, symbol='triangle-up'))])

fig.update_layout(title='EURUSD 4 Hour', xaxis_rangeslider_visible=False)
fig.show()
# fig.append_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']), row=1, col=1)
# fig.append_trace(go.Scatter(x=df.index, y=df['RSI'], mode='lines', name='RSI'), row=2, col=1)
# fig.update_layout(xaxis_rangeslider_visible = False)
# fig.show()