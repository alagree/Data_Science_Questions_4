'''
Download the adjusted close prices for FB, MMM, IBM and AMZN for the last 60 months.
'''
import yfinance as yf
import pandas as pd 

#Create a list of stock names we want to download the adjusted close prices for
stocks_to_import = ['FB','MMM','IBM','AMZN']
adj_close_data = {}
#Iterate across the stock names
for stock in stocks_to_import:
    #Append the adjusted close price of each stock to the dictionary
    adj_close_data[stock] = yf.download(stock, period='5y')['Adj Close'].to_frame()

'''
Resample the data to get prices for the end of the business month. Select the Adjusted Close for each stock.
'''

month_end_data = {stock_name: (values.resample('BM').last()).rename(columns={'Adj Close': 'Mnth_End_Price'}) for stock_name, values in adj_close_data.items()}

'''
Use the pandas autocorrelation_plot() function to plot the autocorrelation of the adjusted month-end close prices for each of the stocks.
Are they autocorrelated?
Provide short explanation.
''' 
import matplotlib.pyplot as plt

#Create a subplot to plot the 4 autocorrelations
fig, axes = plt.subplots(2,2, figsize=(15,15))

#Use pandas to plot the autocorrelation and place a title above each figure
pd.plotting.autocorrelation_plot(month_end_data['FB'],ax=axes[0,0])
axes[0, 0].set_title('Facebook (FB)',size=15)
pd.plotting.autocorrelation_plot(month_end_data['MMM'],ax=axes[0,1])
axes[0, 1].set_title('3M (MMM)',size=15)
pd.plotting.autocorrelation_plot(month_end_data['IBM'],ax=axes[1,0])
axes[1, 0].set_title('International Business Machines (IBM)',size=15)
pd.plotting.autocorrelation_plot(month_end_data['AMZN'],ax=axes[1,1])
axes[1,1].set_title('Amazon (AMZN)',size=15)

'''
Yes to some extent each of the stocks are autocorrelated.
FB:
    There is a statistically significant positive correlation up to ~9 months and negative correlation between 
    ~45 - 53 months.
MMM:
    There is a statistically significant positive correlation up to ~8 months and negative correlation between 
    ~16 - 29 months.  
IBM:
    There is a statistically significant positive correlation up to ~3 months.
AMZN:
    There is a statistically significant positive correlation up to ~10 months and negative correlation between 
    ~38 - 52 months.     
'''

'''
Calculate the monthly returns for each stock using the "shift trick" explained in the lecture, using shift() function.
Use pandas autotocorrelation_plot() to plot the autocorrelation of the monthly returns.
Are the returns autocorrelated? Provide short explanation.
'''
monthly_returns = {stock_name: ((values-values.shift(1)).dropna()).rename(columns={'Mnth_End_Price':'Mnth_End_Return'}) for stock_name, values in month_end_data.items()}

#Create a subplot to plot the 4 autocorrelations
fig, axes = plt.subplots(2,2, figsize=(15,15)) 

#Use pandas to plot the autocorrelation and place a title above each figure
pd.plotting.autocorrelation_plot(monthly_returns['FB'],ax=axes[0,0])
axes[0, 0].set_title('Facebook (FB)',size=15)
pd.plotting.autocorrelation_plot(monthly_returns['MMM'],ax=axes[0,1])
axes[0, 1].set_title('3M (MMM)',size=15)
pd.plotting.autocorrelation_plot(monthly_returns['IBM'],ax=axes[1,0])
axes[1, 0].set_title('International Business Machines (IBM)',size=15)
pd.plotting.autocorrelation_plot(monthly_returns['AMZN'],ax=axes[1,1])
axes[1,1].set_title('Amazon (AMZN)',size=15)

'''
No, the monthly returns are not autocorrelated. As none of the spikes in the figures are above or below the 95%
confidence intervals, there are no statistically significant results. These results suggests that the monthly 
returns of the four stocks do not display a pattern and are randomly distributed.
'''

'''
Combine all 4 time series (returns) into a single DataFrame,
Visualize the correlation between the returns of all pairs of stocks using a scatter plot matrix (use scatter_matrix() function from pandas.plotting).
Explain the results. Is there any correlation?
'''
combined_returns = pd.DataFrame()
for key, values in monthly_returns.items():
    combined_returns[key] = monthly_returns[key]['Mnth_End_Return']

pd.plotting.scatter_matrix(combined_returns, figsize=(10,10))

'''
The pandas scatter matrix function plots a)the distribution of the variables (monthly returns) along the diagonal
and b)correlation plots between each of the monthly return variables. First, we see that the monthly returns are
generally, normally distributed. Furthermore, we see that there are some stocks that display a positive  
correlation in monthly returns. These include: FB and AMZN, IBM and MMM, IBM and AMZN. These results suggest
that as one stocks monthly returns increase the other also increases. However, this relationship is not causal,
meaning that one stock's monthly return does not cause the other to increase. 
'''















