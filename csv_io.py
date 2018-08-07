import pandas as pd


# Load airport codes
def load_airport():
    airport_csv = '../Lookup Tables/L_AIRPORT_ID.csv'
    airport_df = pd.read_csv(airport_csv)
    print(airport_df.head(5))

    return(airport_df)

# Load carrier codes
def load_carrier():
    carrier_csv = '../Lookup Tables/L_CARRIER_HISTORY.csv'
    carrier_df = pd.read_csv(carrier_csv)
    print(carrier_df.head(5))

    return(carrier_df)

# Load mothly data to form a year
def load_monthly():
    month_csv = '../Monthly Data/%d.csv'
    MONTHS = 12

    print('Loading', MONTHS,'months of data')
    month_df = []
    df_len = 0
    for m in range(1,MONTHS+1):
        print('Loaded month:',m)
        next_df = pd.read_csv(month_csv % m)
        month_df.append(next_df)
        df_len += len(next_df)

    year_df = pd.concat(month_df)
    print('Made full year dataframe')

    if df_len != len(year_df):
        raise('Error: Lost rows in merge')

    #remove column due to extranious comma at the end of monthly csv
    year_df.pop('Unnamed: 50')
    year_df['FL_DATE'] = pd.to_datetime(year_df['FL_DATE'])
    print(year_df.head(5))

    return(year_df)




