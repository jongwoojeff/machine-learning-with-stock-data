# machine-learning-with-stock-data
This is a ML model built using [S&P 500](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies) stock data. S&P 500 stock data are pulled using [Yahoo-Finance API](https://rapidapi.com/apidojo/api/yahoo-finance1?utm_source=google&utm_medium=cpc&utm_campaign=1674315309_77004833236&utm_term=yahoo%20finance%20api_e&utm_content=1t1&gclid=EAIaIQobChMIwrmtmMro5QIVASUrCh3MFAIvEAAYASAAEgIejfD_BwE)

## Getting Started
This is a Python based project and I highly recommend you to use [Anaconda platform](https://www.anaconda.com/) since it allows you to handle python modules with ease. 

### Prerequisites
1. A decent Python platform with fundamental Python Knowledge
2. Basic API knowledge
3. Python Modules
   - Numpy
   - Pandas
   - Pandas-datareader
   - Matplotlib
   - BeautifulSoup4
   - sklearn (scikit-learn)
   - yfinance (yahoo-finance)
   
## Machine Learning Details
### Model Type
Supervised with classified outputs (buy, hold, sell)

### Methods used
1. cross_validation; allows us to create shuffled training and testing samples. This is important since we can avoid testing the alogrithm on the same data as we used for training.
2. LinearSVC, KNeighborsClassifier, RandomForestClassifier; classifiers used to predict.
3. VotingClassifier; lets all 3 classifiers above to vote on what each thinks the class is for the feature sets.

### Feature Engineering
1. Remove unecessary data; we only need adj_close column since we want to predict based on previous closed values.
2. Generate a correlation table to see if you can identify any relationships.
3. Fill in the missing data with 0. Some companies may not have existed nor gone public in the time period we have chosen to get data.
4. Our features are the pricing changes(in percentage) from the previous day for all companies. Therefore, we normalize it.
5. Some normalized values will be infinite due to the 0 values that we've previously filled; convert these to NaNs and drop them later. 
6. Our labels will be 1, 0, and -1 which indicate buy, hold, and sell.


## Acknowledgement
- [Sentdex](https://github.com/Sentdex)
