import pandas as pd

class Insights():

    def __init__(self, answers_txt_file='answers.txt'):
       self.answers = open(answers_txt_file, 'w+')
       self.answers.write("\n\nINSIGHTS\n\n")

    def group_sort_agg(self, df, groupby_col_list, agg_col, agg_func, col_name, asc=False):
        sorted_df = df \
                 .groupby(groupby_col_list)[agg_col] \
                 .agg(agg_func) \
                 .reset_index() \
                 .sort_values([col_name], ascending=asc) \
                 .reset_index(drop=True)
        return(sorted_df)

    # I1. Understand airline cancelations? 
    def insight1(self, year_df, carrier_df):
        cancelations_mean = self.group_sort_agg(year_df,'UNIQUE_CARRIER','CANCELLED',['mean','sum'],'mean')
        named_cancelations_mean = cancelations_mean \
                                  .merge(carrier_df, how='left', left_on='UNIQUE_CARRIER', right_on='Code') \
                                  .drop('Code',1)
        return(named_cancelations_mean)

    # I2. Understand airline travel distance? 
    def insight2(self, year_df, carrier_df):
        travel_miles = self.group_sort_agg(year_df,'UNIQUE_CARRIER','DISTANCE',['sum','mean','count'],'mean')
        named_travel_miles = travel_miles \
                             .merge(carrier_df, how='left', left_on='UNIQUE_CARRIER', right_on='Code') \
                             .drop('Code',1)
        return(named_travel_miles)

    # I3. Understand airport's affect on delays? 
    def insight3(self, year_df, airport_df, carrier_df):
        # Rank airports in order of delays
        airport_delay = self.group_sort_agg(year_df,'ORIGIN_AIRPORT_ID','DEP_DELAY_NEW',['mean'],'mean')
        airport_delay['dly_rank']=airport_delay['mean'].rank(ascending=1)
        airport_delay = airport_delay.drop('mean',1)

        # Get airport hubs for each airline
        airport_carrier_delay = self.group_sort_agg(year_df,['ORIGIN_AIRPORT_ID','UNIQUE_CARRIER'],'DEP_DELAY_NEW',['count'],'count')
        hub_delay = airport_carrier_delay[airport_carrier_delay['count']>365]
        hub_delay = hub_delay.drop('count',1)

        hub_delay_ranked = airport_delay.merge(hub_delay, how='right', on='ORIGIN_AIRPORT_ID')
        hub_delay_idx = self.group_sort_agg(hub_delay_ranked,'UNIQUE_CARRIER','dly_rank',['mean'],'mean')
        hub_delay_idx_named = hub_delay_idx \
                             .merge(carrier_df, how='left', left_on='UNIQUE_CARRIER', right_on='Code') \
                             .drop('Code',1)
        return(hub_delay_idx_named)
