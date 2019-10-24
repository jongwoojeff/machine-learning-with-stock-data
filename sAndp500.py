#BeautifulSoup is for5 HTML parsing; getting tickers/symbols from wikipedia
#Pickle for saving the s&p 500 list
import bs4 as bs
import pickle
import requests
import datetime as dt
import os
import pandas as pd
# import pandas_datareader.data as web
import yfinance as yf
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

style.use('ggplot')

yf.pdr_override()


#td stands for table data
#tr stands for table row
#find table name that contains data from wiki source: "wikitable sortable"
def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        ticker = ticker.strip('\n')    #required since every element within tickers contain '\n'
        ticker = str(ticker).replace('.','-') #some tickers with dots and dashes causes problem while searching
        tickers.append(ticker)

    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)

    print(tickers)
    return tickers

# save_sp500_tickers()
# create stock_dfs folder before else throws EOF error
def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2000, 1, 1)
    end = dt.datetime.now()
    for ticker in tickers:
        print(ticker)
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = pdr.get_data_yahoo(ticker, start, end)
            # df.reset_index(inplace=True)
            # df.set_index("Date", inplace=True)
            # df = df.drop("Symbol", axis=1)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

# get_data_from_yahoo()
def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)
    main_df = pd.DataFrame()

    for count,ticker in enumerate(tickers):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)

        df.rename(columns={'Adj Close': ticker}, inplace=True) #renaming adj close column to whatever ticker is
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if count % 10 == 0:
            print(count)

    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')

# compile_data()
def visualize_data():
    df = pd.read_csv('sp500_joined_closes.csv')
    df_corr = df.corr()
    print(df_corr.head())
    df_corr.to_csv('sp500corr.csv')

    #generate heatmap
    data1 = df_corr.values
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)

    heatmap1 = ax1.pcolor(data1, cmap=plt.cm.RdYlGn)
    fig1.colorbar(heatmap1)

    ax1.set_xticks(np.arange(data1.shape[1]) + 0.5, minor=False)
    ax1.set_yticks(np.arange(data1.shape[0]) + 0.5, minor=False)
    ax1.invert_yaxis() #becomes easier to read if we flip y axis
    ax1.xaxis.tick_top() #same reason as above
    column_labels = df_corr.columns #add company names
    row_labels = df_corr.index #column labels and row labels are identical
    ax1.set_xticklabels(column_labels)
    ax1.set_yticklabels(row_labels)
    plt.xticks(rotation=90) #becomes easier to read labels
    heatmap1.set_clim(-1,1)
    plt.tight_layout()
    plt.savefig("correlations.png", dpi = (300))
    # plt.show()

# visualize_data()

# features = daily pricing changes of all companies
def process_data_for_labels(ticker):
    hm_days = 7
    df = pd.read_csv('sp500_joined_closes.csv', index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)

    for i in range(1,hm_days+1):
        df['{}_{}d'.format(ticker,i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]

    df.fillna(0, inplace=True)
    return tickers, df
