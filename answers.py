


class answers():

    def __init__(self, answers_txt_file='answers.txt'):
       self.answers = open(answers_txt_file, 'w+')

    def group_sort(df, groupby_col_list, agg_col, agg_func, col_name=agg_func, asc=False):
        sorted_df = df \
                 .groupby(groupby_col_list)[agg_col] \
                 .agg(agg_func) \
                 .reset_index(name=col_name) \
                 .sort_values([col_name], ascending=asc) \
                 .reset_index(drop=True)
        return(sorted_df)

    # Q1. What is the 15th most flown route? 
    def answer1(self):
        self.answers.write('Q1. What is the 15th most flown route?'+'\n'))
        FLOWN_RANK = 15

        routes = group_sort(year_df,['ORIGIN_AIRPORT_ID','DEST_AIRPORT_ID'],'FL_DATE',count(),'count')

        routes = year_df \
                 .groupby(['ORIGIN_AIRPORT_ID','DEST_AIRPORT_ID'])['FL_DATE'] \
                 .agg('count') \
                 .reset_index(name='count') \
                 .sort_values(['count'], ascending=False) \
                 .reset_index(drop=True)

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


    # Q2. What carrier has flown the 3rd most number of flights? How many? 
    def answer2(self):
        self.answers.write('Q2. What carrier has flown the 3rd most number of flights? How many?'+'\n'))
        CARRIER_RANK = 3

        carriers = year_df \
                 .groupby('UNIQUE_CARRIER')['FL_DATE'] \
                 .count() \
                 .reset_index(name='count') \
                 .sort_values(['count'], ascending=False) \
                 .reset_index(drop=True)

        named_carriers = carriers \
                       .merge(carrier_df, how='left', left_on='UNIQUE_CARRIER', right_on='Code') \
                       .drop('Code',1)

        carrier_3 = named_carriers.loc[CARRIER_RANK-1]
        q2_answer = ('The 3rd most popular carrier was '
                     '{} with {} flights in 2014'
                     .format(carrier_3.Description,carrier_3['count']))
        self.answers.write(q2_answer+'\n\n'))


    # Q3. What airport has the 10th most delays?
    def answer3(self):
        self.answers.write('Q3. What airport has the 10th most delays?'+'\n'))
        DELAYS_RANK = 10

        airport_dlys = year_df[year_df['DEP_DELAY_NEW']>0].groupby('ORIGIN_AIRPORT_ID')

        airport_dlys_count = airport_dlys['DEP_DELAY_NEW'] \
                            .count() \
                            .reset_index(name='count') \
                            .sort_values(['count'], ascending=False) \
                            .reset_index(drop=True)

        named_airport_dlys_count = airport_dlys_count \
                                   .merge(airport_df, how='left', left_on='ORIGIN_AIRPORT_ID', right_on='Code') \
                                   .drop('Code',1)
        airport_count_10 = named_airport_dlys_count.loc[DELAYS_RANK-1]
        q3_answer_count = ('The airport with the 10th most delays according to counts was '
                           '{} with {} delays in 2014'
                           .format(airport_mean_10.Description,airport_mean_10['count']))
        self.answers.write(q3_answer_count+'\n')

        airport_dlys_mean = airport_dlys['DEP_DELAY_NEW'] \
                            .mean() \
                            .reset_index(name='dly_mean') \
                            .sort_values(['dly_mean'], ascending=False) \
                            .reset_index(drop=True)

        named_airport_dlys_mean = airport_dlys_mean \
                                  .merge(airport_df, how='left', left_on='ORIGIN_AIRPORT_ID', right_on='Code') \
                                  .drop('Code',1)
        airport_mean_10 = named_airport_dlys_mean.loc[DELAYS_RANK-1]
        q3_answer_mean = ('The airport with the 10th most delays according to the mean was '
                          '{} with a mean delay of {} minutes'
                          .format(airport_mean_10.Description,airport_mean_10['dly_mean']))
        self.answers.write(q3_answer_mean+'\n\n')


    # Q4. What is the second most popular day of the week to travel? Why? 
    def answer4(self):
        answers.write('Q4. What is the second most popular day of the week to travel? Why? '+'\n'))
        DELAYS_RANK = 10

