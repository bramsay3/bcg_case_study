
class Insights():

    def __init__(self, answers_txt_file='answers.txt'):
       self.answers = open(answers_txt_file, 'w+')
       self.answers.write("\n\nINSIGHTS\n\n")

    def group_sort_agg(df, groupby_col_list, agg_col, agg_func, col_name, asc=False):
        sorted_df = df \
                 .groupby(groupby_col_list)[agg_col] \
                 .agg(agg_func) \
                 .reset_index() \
                 .sort_values([col_name], ascending=asc) \
                 .reset_index(drop=True)
        return(sorted_df)

    # I1. Understand airline cancelations? 
    def insight1(self, year_df, carrier_df):
        self.answers.write('I1. Understand airline cancelations?'+'\n')

        cancelations_mean = group_sort_agg(year_df,'UNIQUE_CARRIER','CANCELLED',['mean','count'],'mean')
        named_cancelations_mean = cancelations_mean \
                                  .merge(carrier_df, how='left', left_on='UNIQUE_CARRIER', right_on='Code') \
                                  .drop('Code',1)

        FL = named_cancelations_mean.loc[4]
        F9 = named_cancelations_mean.loc[12]


        ins1 = """The data indicates that smaller airlines cannot cancel very many flights. 
                In 2014 {} operated {} flights and canceled {} percent of their flights and went out of buissiness in 2014. 
                {} was cancelling a higher portion of their flights then 6 larger airlines. 
                At the same time {} operated {} flights and only canceled {} percent of their flights.""".format(FL['Description'],FL['count'],FL['mean'],FL['Description'],F9['Description'],F9['count'],F9['mean'])
                self.answers.write(q1_answer+'\n\n')

    # I2. Understand airline travel distance? 
    def insight2(self, year_df, carrier_df):
        self.answers.write('I2. Understand airline travel distance?'+'\n')

        travel_miles = group_sort_agg(year_df,'UNIQUE_CARRIER','DISTANCE',['sum','mean','count'],'mean')
        named_travel_miles = travel_miles \
                             .merge(carrier_df, how='left', left_on='UNIQUE_CARRIER', right_on='Code') \
                             .drop('Code',1)

    # I3. Understand airport's affect on delays? 
    def insight2(self, year_df, airport_df):
self.answers.write('I2. Understand airline travel distance?'+'\n')

airport_delay = group_sort_agg(year_df,'ORIGIN_AIRPORT_ID','DEP_DELAY_NEW',['mean','std','count'],'mean')
named_airport_delay = airport_delay \
                     .merge(airport_df, how='left', left_on='ORIGIN_AIRPORT_ID', right_on='Code') \
                     .drop('Code',1)
named_airport_delay['dly_rank']=named_airport_delay['mean'].rank(ascending=1)


airport_delay = group_sort_agg(year_df,['ORIGIN_AIRPORT_ID','UNIQUE_CARRIER'],'DEP_DELAY_NEW',['mean','std','count'],'mean')
named_airport_delay = airport_delay \
                     .merge(airport_df, how='left', left_on='ORIGIN_AIRPORT_ID', right_on='Code') \
                     .drop('Code',1)
named_hub_delay = named_airport_delay[named_airport_delay[count]>100]







if __name__=='__main__':
    import csv_io
    import pandas as pd
    airport_df = csv_io.load_airport()
    carrier_df = csv_io.load_carrier()
    year_df = csv_io.load_monthly()

    ins = Insights()
    ins.insight1(year_df, airport_df)









