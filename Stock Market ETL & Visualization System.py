#import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import boto3

#storing stocks name in a list
tickers = ['Jpm','Bac','C']

jpm_path = "JPM.csv"
c_path = "C.csv"
bac_path = "BAC.csv"

jpm_df = pd.read_csv(jpm_path)
c_df = pd.read_csv(c_path)
bac_df = pd.read_csv(bac_path)

jpm_df = jpm_df.add_prefix('JPM_')
bac_df = bac_df.add_prefix('BAC_')
c_df = c_df.add_prefix('C_')

jpm_df['JPM_Date'] = pd.to_datetime(jpm_df['JPM_Date'])  # Convert to datetime if necessary
jpm_df.set_index('JPM_Date', inplace=True)

bac_df['BAC_Date'] = pd.to_datetime(bac_df['BAC_Date'])
bac_df.set_index('BAC_Date', inplace=True)

c_df['C_Date'] = pd.to_datetime(c_df['C_Date'])
c_df.set_index('C_Date', inplace=True)

jpm_close = jpm_df[['JPM_Close']]
bac_close = bac_df[['BAC_Close']]
c_close = c_df[['C_Close']]

bank_data = pd.concat([jpm_close, bac_close, c_close], axis=1)

column_names = tickers.copy()
bank_data.columns = column_names


#pd.DataFrame(bank_data)
plt.figure(figsize = (18,12))
plt.boxplot(bank_data)
plt.title('Boxplot of Bank Stock Prices (5Y Lookback)', fontsize = 15)
plt.ylabel('Stock Price',fontsize = 15)
plt.xlabel('Banks', fontsize = 15)
labels = ['JPM','BAC', 'C']
plt.xticks(range(1, len(bank_data.columns) + 1), list(bank_data.columns), fontsize=12)


#ploting a Scatter Graph for BAC Bank stocks
# we store the dates in a series frame in pandas 1 d array
dates = bank_data.index.to_series()
plt.figure(figsize = (18,12))
plt.scatter(dates,bac_close)
plt.title('Scatter Plot of Bank Stock Prices (5Y Lookback)',fontsize = 15)
plt.xlabel('Dates', fontsize = 15)
plt.ylabel('Prices', fontsize = 15)


#plotting Histogram for all the banks stovks data collected
plt.figure(figsize = (18,12))
plt.hist(bank_data, bins = 50)
plt.legend(bank_data.columns, fontsize = 12)
plt.title(' Histogram of Bank Stock Prices (5Y Lookback)',fontsize = 15)
plt.xlabel('Stock Price',fontsize = 15)
plt.ylabel('Observation',fontsize = 15)

#ploting scatter graph for c 
plt.figure(figsize = (18,12))
plt.scatter(dates,c_close)
plt.title('Scatter Plot of  C Bank Stock Prices (5Y Lookback)',fontsize = 15)
plt.xlabel('Dates', fontsize = 15)
plt.ylabel('Prices', fontsize = 15)


#subplottigg
plt.subplot(2,2,1)
#plt.figure(figsize = (18,12))
plt.boxplot(bank_data)
plt.title('Boxplot of Bank Stock Prices (5Y Lookback)', fontsize = 15)
plt.ylabel('Stock Price',fontsize = 15)
plt.xlabel('Banks', fontsize = 15)
labels = ['JPM','BAC', 'C']
plt.xticks(range(1, len(bank_data.columns) + 1), list(bank_data.columns), fontsize=12)


plt.subplot(2,2,2)
#ploting a Scatter Graph for BAC Bank stocks
# we store the dates in a series frame in pandas 1 d array
dates = bank_data.index.to_series()
#plt.figure(figsize = (18,12))
plt.scatter(dates,bac_close)
plt.title('Scatter Plot of Bank Stock Prices (5Y Lookback)',fontsize = 15)
plt.xlabel('Dates', fontsize = 15)
plt.ylabel('Prices', fontsize = 15)


plt.subplot(2,2,3)
#plotting Histogram for all the banks stovks data collected
#plt.figure(figsize = (18,12))
plt.hist(bank_data, bins = 50)
plt.legend(bank_data.columns, fontsize = 12)
plt.title(' Histogram of Bank Stock Prices (5Y Lookback)',fontsize = 15)
plt.xlabel('Stock Price',fontsize = 15)
plt.ylabel('Observation',fontsize = 15)

plt.subplot(2,2,4)
#ploting scatter graph for c 
#plt.figure(figsize = (18,12))
plt.scatter(dates,c_close)
plt.title('Scatter Plot of  C Bank Stock Prices (5Y Lookback)',fontsize = 15)
plt.xlabel('Dates', fontsize = 15)
plt.ylabel('Prices', fontsize = 15)

plt.tight_layout()

plt.savefig('bank_data.png')
 
#uploading our visualization to AWS S3
s3 = boto3.resource('s3')
s3.meta.client.upload_file('bank_data.png', 'your_bucket', 'bank_data.png', ExtraArgs={'ACL':'public-read'})
