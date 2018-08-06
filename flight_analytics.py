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
MONTHS = 12
year_df = pd.read_csv(month_csv % 1)
print('Loading', MONTHS,'months (might take a few minutes)')
print('Loaded month: 1')
df_len = len(year_df)
for m in range(2,MONTHS+1):
    print('Loaded month:',m)
    next_df = pd.read_csv(month_csv % m)
    year_df = pd.merge(year_df, next_df, how='outer')
    df_len += len(next_df)

if df_len != len(year_df):
    raise('Error: Lost rows in merge')

#remove column due to extranious comma at the end of monthly csv
year_df.pop('Unnamed: 50')
print(year_df.head(5))


answers = open('answers.txt', 'w+')

# Q1. What is the 15th most flown route? 
answers.write('Q1. What is the 15th most flown route?\n')
WANTED_RANK = 15

routes = year_df \
         .groupby(['ORIGIN_AIRPORT_ID','DEST_AIRPORT_ID'])['FL_DATE'] \
         .count() \
         .reset_index(name='count') \
         .sort_values(['count'], ascending=False) \
         .reset_index(drop=True)

named_routes = routes \
               .merge(airport_df, how='left', left_on='ORIGIN_AIRPORT_ID', right_on='Code') \
               .drop('Code',1) \
               .merge(airport_df, how='left', left_on='DEST_AIRPORT_ID', right_on='Code', suffixes=('_start','_end')) \
               .drop('Code',1)

route_15 = named_routes.loc[WANTED_RANK-1]
q1_answer = ('The 15th most common route was '
             'from {} to {} with {} flights in 2014'
             .format(route_15.Description_start,route_15.Description_end,route_15['count']))
answers.write(q1_answer+'\n')


# Q2. What carrier has flown the 3rd most number of flights? How many? 
answers.write('Q2. What carrier has flown the 3rd most number of flights? How many?\n')

















