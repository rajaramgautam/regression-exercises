import pandas as pd
import numpy as np
import os
from env import host, user, password

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

# Remove the angry pink boxes
import warnings
warnings.filterwarnings("ignore")



def get_connection(db, user=user, host=host, password=password):
    '''
    This function uses my info from my env file to
    create a connection url to access the Codeup server and we will retrieve data from zillow database.
    It takes in a string name of a database as an argument.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

    
def new_zillow_data():
    '''
    This function reads the reads zillow database data from the Codeup Server into a df,
    write it to a csv file, and returns the df.
    '''
    # Create SQL query.
    sql_query = """ 
    SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
FROM properties_2017

JOIN propertylandusetype USING(propertylandusetypeid)

WHERE propertylandusedesc IN ("Single Family Residential",                       
                              "Inferred Single Family Residential")
    """
    
    
    # Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_connection('zillow'))
    
    # Converting columns into readable format
    df = df.rename(columns = {'bedroomcnt':'bedrooms', 
                          'bathroomcnt':'bathrooms', 
                          'calculatedfinishedsquarefeet':'area',
                          'taxvaluedollarcnt':'tax_value', 
                          'yearbuilt':'year_built'})
    # dropping null from df
    df = df.dropna()
    
    # Changing datatypes of the columns

    df['bedrooms']= df.bedrooms.astype('int')
    df['year_built'] = df.year_built.astype('int')
    df['fips'] = df.fips.astype('object')

    # dropping rows with absured meaning
    df = df[df.bathrooms > 0]
    df = df[df.bedrooms > 0]
    
    return df

def get_histogram(df):
    
    plt.figure(figsize=(16, 3))

    # List of columns
    cols = ['bedrooms', 'bathrooms', 'area', 'tax_value', 'taxamount']

    for i, col in enumerate(cols):
    
        # i starts at 0, but plot nos should start at 1
        plot_number = i + 1 
    
        # Create subplot.
        plt.subplot(1, 5, plot_number)
    
        # Title with column name.
        plt.title(col)
    
        # Display histogram for column.
        df[col].hist(bins= 5, edgecolor='black')
    

    
        # Hide gridlines.
        plt.grid(False)
        
def get_boxplot(df):        
    # List of columns
    cols = [col for col in df.columns if col not in ['fips', 'year_built']]
    plt.figure(figsize=(16, 20))
    for i, col in enumerate(cols):

        # i starts at 0, but plot nos should start at 1
        plot_number = i + 1 

        # Create subplot.
        plt.subplot(1, len(cols), plot_number)

        # Title with column name.
        plt.title(col)

        # Display boxplot for column.
        sns.boxplot(data=df[cols])
    

        # Hide gridlines.
        plt.grid(False)

    plt.show()
    
def prepare_zillow(df):
    ''' Prepare zillow data for exploration'''

    # removing outliers
    df = remove_outliers(df, 1.5, ['bedrooms', 'bathrooms', 'area', 'tax_value', 'taxamount'])
    
    # get distributions of numeric data
    get_histogram(df)
    get_boxplot(df)
    
    
    # train/validate/test split
    train_validate, test = train_test_split(df, test_size=.2, random_state=123)
    train, validate = train_test_split(train_validate, test_size=.3, random_state=123)
          
    
    return train, validate, test 


def remove_outliers(df, k, col_list):
    ''' remove outliers from a list of columns in a dataframe 
        and return that dataframe
    '''
    
    for col in col_list:

        q1, q3 = df[col].quantile([.25, .75])  # get quartiles
        
        iqr = q3 - q1   # calculate interquartile range
        
        upper_bound = q3 + k * iqr   # get upper bound
        lower_bound = q1 - k * iqr   # get lower bound

        # return dataframe without outliers
        
        df = df[(df[col] > lower_bound) & (df[col] < upper_bound)]
        
    return df


def wrangle_zillow():
    '''Acquire and prepare data from Zillow database for explore'''
    train, validate, test = prepare_zillow(new_zillow_data())
    
    return train, validate, test