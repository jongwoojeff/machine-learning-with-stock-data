import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web



#style setting for pretty graphs
style.use('ggplot')

start = dt.datetime(2015, 1, 1)
end = dt.datetime.now()

#using yahoo to gather data
df = web.DataReader("TSLA", 'yahoo', start, end)
df.to_csv('TSLA.csv')
df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)

#Adj close ccounts for future stick splits and provides relative price to splits.
#therefore, use only Adj close for data manipulation
# df['Adj Close'].plot()
# plt.show()

#100 days rolling moving average for average price
#without min_periods setting, NaN will appear for the first 100ma since there aren't any 100 prior data points
df['100ma'] = df['Adj Close'].rolling(window=100,min_periods=0).mean()
print(df.head())

#ax1, red line, Adj Close
#ax2, blue line, 100ma
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Volume'])

plt.show()

#check changes
#messing around