import pandas as pd
import numpy as np
import os
from env import host, user, password

###################### Acquire Zillow Data ######################

def get_connection(db, user=user, host=host, password=password):
    '''
    This function uses my info from my env file to
    create a connection url to access the Codeup db.
    It takes in a string name of a database as an argument.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'
    
    
    
def new_zillow_data():
    '''
    This function reads the reads zillow database data from the Codeup Server into a df,
    write it to a csv file, and returns the df.
    '''
    # Create SQL query.
    sql_query = 'select bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips  from properties_2017 where propertylandusetypeid = 261;'
    
    # Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_connection('zillow'))
    
    return df



def get_zillow_data():
    '''
    This function reads in zillow data from Codeup database, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''
    if os.path.isfile('df.csv'):
        
        # If csv file exists, read in data from csv file.
        df = pd.read_csv('df.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame.
        df = new_zillow_data()
        
        # Write DataFrame to a csv file.
        df.to_csv('df.csv')
        
    return df

def wrangle_zillow(df):
    """
    This functions drops null in zillow data.
    """
    df = df.dropna()
    df['bedroomcnt']= df.bedroomcnt.astype('int')
    df['yearbuilt'] = df.yearbuilt.astype('int')
    
    return df
    