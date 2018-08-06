import pandas as pd


# Load airport codes
airport_csv = '../Lookup Tables/L_AIRPORT_ID.csv'
airport_df = pd.read_csv(airport_csv)
print(airport_df.head(5))

# Load carrier codes
carrier_csv = '../Lookup Tables/L_CARRIER_HISTORY.csv'
carrier_df = pd.read_csv(carrier_csv)
print(carrier_df.head(5))

# Load mothly data to form a year
month_csv = '../Monthly Data/%d.csv'
months = 12
year_df = pd.read_csv(month_csv % 1)
print('Loading', months,'months (might take a few minutes)')
print('Loaded month: 1')
df_len = len(year_df)
for m in range(2,months+1):
    print('Loaded month:',m)
    next_df = pd.read_csv(month_csv % m)
    year_df = pd.merge(year_df, next_df, how='outer')
    df_len += len(next_df)

if df_len != len(year_df):
    raise('Error: Lost rows in merge')

#remove column due to extranious comma at the end of monthly csv
year_df.pop('Unnamed: 50')
print(year_df.head(5))

# Q1. What is the 15th most flown route? 





