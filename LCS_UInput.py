import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#this function is to get the uder time that we will use for exploring data
def get_time_period():
    period_options = ['month', 'year', 'none']
    month_options = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    year_options = ['2016', '2017']

    print('Hello, in this script you will be able to get details about London stop and search data!')
    print('\nFirst thing that we want to do is see what time period you want to view the information for.')
    print('\nBy default we will range from January 2016 to April 2017, but you have the option to filter the data')

    #This will ask for an input to see how the user wants to search the data. The loop merely ensures that what we select is supported.
    while True:
        try:
            period_input = str(input('\nYou can filter by month, year or not at all. If you want no filter, type "none":\n'))
        except ValueError:
            print('{} was sadly not understood'.format(period_input))
            continue
        if period_input.lower() not in period_options:
            print('Sadly {}} was not an option'.format(period_input))
            continue
        else:
            period = period_input.lower()
            break
    #if the user has selected to filter on months, we need to know what months they want to filter on
    if period == 'month':
        while True:
            try:
                month_input = str(input('\nYou have selected to filter by month - lets see what month you want to look at!'))
            except ValueError:
                print('{} was sadly not understood'.format(month_input))
                continue
            if month_input.lower() not in month_options:
                print('Apologies, {} is not actually a month....'.format(month_input))
                continue
            else:
                month = month_input.lower()
                year = 'all'
                break
    #if the user wants to search by year, lets find out what year
    elif period == 'year':
        while True:
            try:
                year_input = str(input('\nSo you want to search by year (remember we only have a few month for 2017), what year shall we search on?'))
            except ValueError:
                print('{} that is not a legitimate thing to enter'.format(year_input))
                continue
            if year_input.lower() not in year_options:
                print('{} that was not a year on the list, its 2016 or 2017...'.format(year_input))
                continue
            else:
                year = year_input.lower()
                month = 'all'
                break
    #if they dont select month or year than we need to set those variables to show all
    else:
        print('You want to search on all data then? Nice.')
        month = 'all'
        year = 'all'

    return period, month, year

#if we filter the data it becomes so much easier to do analysis on
def load_data(period, month, year):
    #load the dataset from Kaggle (https://www.kaggle.com/sohier/london-police-records)
    df = pd.read_csv('/Users/oliverphipps/Dropbox/6. Python/Python Projects/LondonCrimeStatistics/london-stop-and-search.csv')

    #as I have done analysis on this already via Jupyter notebooks I know that I have to clean this data
    #renaming columns to something more applicable
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    #removing uneccesary columns
    df.drop(['policing_operation', 'self-defined_ethnicity', 'part_of_a_policing_operation', 'latitude', 'longitude', 'outcome_linked_to_object_of_search', 'removal_of_more_than_just_outer_clothing'], axis=1, inplace=True)

    #renaming a column to make it easier to search
    df.rename({'officer-defined_ethnicity':'ethnicity'}, axis=1, inplace=True)

    #putting the date field in a better format
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.date

    #drop na's
    df_clean = df.dropna()

    #remove all data for 2015 as it is not useful for analysis
    df['date'] = pd.to_datetime(df['date'])
    df_clean = df[df['date'].dt.year != 2015]
    df_clean = df_clean.dropna()

    #make some columns for the filtering
    df_clean['month'] = df_clean['date'].dt.month
    df_clean['year'] = df_clean['date'].dt.year

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july','august', 'september', 'october', 'november', 'december']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df_clean = df_clean[df_clean['month'] == month]

    # filter by day of week if applicable
    if year != 'all':
        # filter by day of week to create the new dataframe
        df_clean = df_clean[df_clean['year'] == year]

    return df_clean
