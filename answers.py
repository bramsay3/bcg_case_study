
import pandas as pd

class Answers():

    def __init__(self, answers_txt_file='answers.txt'):
       self.answers = open(answers_txt_file, 'w+')
       self.answers.write("\n\nQUESTIONS\n\n")

    def group_sort_agg(self, df, groupby_col_list, agg_col, agg_func, col_name, asc=False):
        sorted_df = df \
                 .groupby(groupby_col_list)[agg_col] \
                 .agg(agg_func) \
                 .reset_index(name=col_name) \
                 .sort_values([col_name], ascending=asc) \
                 .reset_index(drop=True)
        return(sorted_df)

    # Q1. What is the 15th most flown route? 
    def answer1(self, year_df, airport_df):
        self.answers.write('Q1. What is the 15th most flown route?'+'\n')
        FLOWN_RANK = 15

        routes = self.group_sort_agg(year_df,['ORIGIN_AIRPORT_ID','DEST_AIRPORT_ID'],'FL_DATE','count','count')

        named_routes = routes \
                       .merge(airport_df, how='left', left_on='ORIGIN_AIRPORT_ID', right_on='Code') \
                       .drop('Code',1) \
                       .merge(airport_df, how='left', left_on='DEST_AIRPORT_ID', right_on='Code', suffixes=('_start','_end')) \
                       .drop('Code',1)

        route_15 = named_routes.loc[FLOWN_RANK-1]
        q1_answer = ('The 15th most common route was '
                     'from {} to {} with {} flights in 2014'
                     .format(route_15.Description_start,route_15.Description_end,route_15['count']))
        self.answers.write(q1_answer+'\n\n')
        return(named_routes)


    # Q2. What carrier has flown the 3rd most number of flights? How many? 
    def answer2(self, year_df, carrier_df):
        self.answers.write('Q2. What carrier has flown the 3rd most number of flights? How many?'+'\n')
        CARRIER_RANK = 3

        carriers = self.group_sort_agg(year_df,'UNIQUE_CARRIER','FL_DATE','count','count')

        named_carriers = carriers \
                       .merge(carrier_df, how='left', left_on='UNIQUE_CARRIER', right_on='Code') \
                       .drop('Code',1)

        carrier_3 = named_carriers.loc[CARRIER_RANK-1]
        q2_answer = ('The 3rd most popular carrier was '
                     '{} with {} flights in 2014'
                     .format(carrier_3.Description,carrier_3['count']))
        self.answers.write(q2_answer+'\n\n')
        return(named_carriers)


    # Q3. What airport has the 10th most delays?
    def answer3(self, year_df, airport_df):
        self.answers.write('Q3. What airport has the 10th most delays?'+'\n')
        DELAYS_RANK = 10

        airport_dlys = year_df[year_df['DEP_DELAY_NEW']>0]

        airport_dlys_count = self.group_sort_agg(year_df,'ORIGIN_AIRPORT_ID','DEP_DELAY_NEW','count','count')
        named_airport_dlys_count = airport_dlys_count \
                                   .merge(airport_df, how='left', left_on='ORIGIN_AIRPORT_ID', right_on='Code') \
                                   .drop('Code',1)

        airport_count_10 = named_airport_dlys_count.loc[DELAYS_RANK-1]
        q3_answer_count = ('The airport with the 10th most delays according to counts was '
                           '{} with {} delays in 2014'
                           .format(airport_count_10.Description,airport_count_10['count']))
        self.answers.write(q3_answer_count+'\n')


        airport_dlys_mean = self.group_sort_agg(year_df,'ORIGIN_AIRPORT_ID','DEP_DELAY_NEW','mean','dly_mean')
        named_airport_dlys_mean = airport_dlys_mean \
                                  .merge(airport_df, how='left', left_on='ORIGIN_AIRPORT_ID', right_on='Code') \
                                  .drop('Code',1)

        airport_mean_10 = named_airport_dlys_mean.loc[DELAYS_RANK-1]
        q3_answer_mean = ('The airport with the 10th most delays according to the mean was '
                          '{} with a mean delay of {} minutes'
                          .format(airport_mean_10.Description,airport_mean_10['dly_mean']))
        self.answers.write(q3_answer_mean+'\n\n')

        airport_dly = airport_dlys_count.merge(named_airport_dlys_mean.drop('Description',1), on='ORIGIN_AIRPORT_ID').drop('ORIGIN_AIRPORT_ID',1)


        return(named_airport_dlys_count,named_airport_dlys_mean)


    # Q4. What is the second most popular day of the week to travel? Why? 
    def answer4(self, year_df):
        self.answers.write('Q4. What is the second most popular day of the week to travel?'+'\n')
        TRAVEL_RANK = 2


        year_df['WEEKDAY'] = year_df['FL_DATE'].apply(lambda dt:dt.weekday())
        travel_day = self.group_sort_agg(year_df,'WEEKDAY','FL_NUM','count','count')
        #travel_day['AVG_CANCELLED'] = self.group_sort_agg(year_df,'WEEKDAY','CANCELLED','mean','cancelled_avg')['cancelled_avg']
        weekdays = {'num': list(range(7)), 'day_name': ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']}
        weekday_df = pd.DataFrame(weekdays)
        weekday_cnts = travel_day \
                       .merge(weekday_df, how='left', left_on='WEEKDAY', right_on='num') \
                       .drop('num',1)

        popular_day_2 = weekday_cnts.loc[TRAVEL_RANK-1]

        q4_answer = ('The the 2nd most popular day of the week to travel is '
                           '{} with {} trips in 2014'
                           .format(popular_day_2.day_name,popular_day_2['count']))
        self.answers.write(q4_answer+'\n\n')
        return(weekday_cnts)

if __name__=='__main__':
    import csv_io
    airport_df = csv_io.load_airport()
    carrier_df = csv_io.load_carrier()
    year_df = csv_io.load_monthly()

    ans = Answers()
    ans.answer1(year_df, airport_df)
    ans.answer2(year_df, carrier_df)
    ans.answer3(year_df, airport_df)
    ans.answer4(year_df)
    ans.answers.close()





