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

#from here on in are analysis functions which will show us relevant data
def total_search_breakdown(df_clean):
    count_by_date = df_clean.groupby('date').size()

    print('\nThe below plot shows the count of total stop and search')

    plt.figure(figsize=(20,10))
    plt.xlabel('Date')
    plt.ylabel('Count of Stop and Search Record')
    plt.title('Time series graph showing stop and search activity')
    plt.plot(count_by_date);

def ethnicity_breakdown(df_clean):
    print('\nThe below plot shows the count of stop and search by ethnicity')

    df_clean['ethnicity'].value_counts().plot.bar(title='stop_and_search_by_ethnicity',figsize=(15,10));

def objective_breakdown(df_clean):
    print('\nThe below shoes the count of stop and search by objective')

    df_clean['object_of_search'].value_counts().plot.bar(title='Stop and Search by Object of Search',figsize=(15,10));

    print('\nThe below groups "Controlled Drugs" and "Articles for use in Criminal Damage" and shows them as a percentage of each other')
    counts = df_clean['object_of_search'].value_counts()
    counts[counts > 5000]

    #creating some masks for the two we are ooking for
    drugs = df_clean.object_of_search == 'Controlled drugs'
    criminal_damage = df_clean.object_of_search == 'Articles for use in criminal damage'

    #creating a total that we can use as denominator for the percentage calculator
    drugs_p_crimdam = df_clean.object_of_search[criminal_damage].count() + df_clean.object_of_search[criminal_damage].count()

    #creating some percentages for the pie chart
    drugs_prc = df_clean.object_of_search[drugs].count() / drugs_p_crimdam
    criminal_damage_prc = df_clean.object_of_search[criminal_damage].count() / drugs_p_crimdam

    # this will plot a pie chart for us using the above
    labels = 'Controlled Drugs', 'Articles for use in criminal damage'
    fracs = [drugs_prc, criminal_damage_prc]
    explode = (0,0)
    plt.axis("equal")
    plt.title('Percentage Drug vs. Weapons search as pct of Drugs plus Weapons')
    plt.pie(fracs, explode=explode, labels=labels, autopct='%.0f%%', shadow=True);

def eth_objective_breakdown(df_clean):
    print('\nThe below groups ethnicity and obective breakdowns together to try and show us some trends')

    print('\nFirst by objective of search and then by ethnicity')
    df_clean.groupby('ethnicity')['object_of_search'].value_counts().unstack(0).plot.bar(title='Object of search by Ethnicity', figsize=(15,10));

    print('\nAnd now by ethnicity and then objective of search')
    df_clean.groupby('object_of_search')['ethnicity'].value_counts().unstack(0).plot.bar(title='Ethnicity by Object of Search', figsize=(15,10));

def gender_breakdown(df_clean):
    print('\nThis here will show us a bar chart of Gender by the Objective of search')
    df_clean.groupby('object_of_search')['gender'].value_counts().unstack(0).plot.bar(title='Gender by Object of Search', figsize=(15,10));

    print('\nNow lets see that total stop and search counts by Gender')

    #creating some masks
    gender_male = df_clean.gender == 'Male'
    gender_female = df_clean.gender == 'Female'
    gender_other = df_clean.gender == 'Other'

    #creating percentages
    gender_male_prc = df_clean.gender[gender_male].count() / len(df_clean)
    gender_female_prc = df_clean.gender[gender_female].count() / len(df_clean)
    gender_other_prc = df_clean.gender[gender_other].count() / len(df_clean)

    # this will plot a pie chart for us using the calcs above
    labels = 'Male', 'Female', 'Other'
    fracs = [gender_male_prc, gender_female_prc, gender_other_prc]
    explode = (0.0,0,0)
    plt.axis("equal")
    plt.title('Percentage of Stop and Search by Gender')
    plt.pie(fracs, explode=explode, labels=labels, autopct='%.0f%%', shadow=True);

def age_breakdown(df_clean):
    print('\nNow lets see a gender breakdown by count as percentage of total')

    #as above, lets make some masks
    age_u10 = df_clean.age_range == 'under 10'
    age_10 = df_clean.age_range == '10-17'
    age_18 = df_clean.age_range == '18-24'
    age_25 = df_clean.age_range == '25-34'
    age_34 = df_clean.age_range == 'over 34'

    #and some percentages
    age_u10_prc = df_clean.age_range[age_u10].count() / len(df_clean)
    age_10_prc = df_clean.age_range[age_10].count() / len(df_clean)
    age_18_prc = df_clean.age_range[age_18].count() / len(df_clean)
    age_25_prc = df_clean.age_range[age_25].count() / len(df_clean)
    age_34_prc = df_clean.age_range[age_34].count() / len(df_clean)

     # and a pie chart
    labels = 'Under 10', '10-17', '18-24', '25-34', '35+'
    fracs = [age_u10_prc, age_10_prc, age_18_prc, age_25_prc, age_34_prc]
    explode = (0,0,0,0,0)
    plt.axis("equal")
    plt.title('Percentage of Stop and Search by Age range')
    plt.pie(fracs, explode=explode, labels=labels, autopct='%.0f%%', shadow=True);

    print('\nNow lets analyse this more by looking at age by Objective of search')
    df_clean.groupby('object_of_search')['age_range'].value_counts().unstack(0).plot.bar(title='Age range by Object of Search', figsize=(15,10));

def time_series_graphs(df_clean):
    print('\nWe have looked at top level statistics now, but what is useful is to see how things change over time')
    print('\nFor that lets plot some graphs showing change over time')

    print('\nLets look first at this by Ethnicity')
    #first by ethnicity
    race_count = df_clean.groupby('date')
    race_count = race_count.ethnicity.apply(pd.value_counts).unstack(-1).fillna(0)
    race_count.plot(kind='line',figsize=(20,10), title='Stop and Search Count by Race');

    print('\nNow by objective of search')
    object_count = df_clean.groupby('date')
    object_count = object_count.object_of_search.apply(pd.value_counts).unstack(-1).fillna(0)
    object_count.plot(kind='line',figsize=(20,10), title='Stop and Search Count by Object of Search');

    print('\nAnd by Gender')
    gender_count = df_clean.groupby('date')
    gender_count = gender_count.gender.apply(pd.value_counts).unstack(-1).fillna(0)
    gender_count.plot(kind='line',figsize=(20,10), title='Stop and Search Count by Gender');

    print('\nLastly, age')
    age_count = df_clean.groupby('date')
    age_count = age_count.age_range.apply(pd.value_counts).unstack(-1).fillna(0)
    age_count.plot(kind='line', figsize=(20,10), title='Stop and Search Count by Age');

def random_line(df_clean):
    # this is used to select a random line of data to look at
    df_1 = df_clean.sample(n=1)
    print(df_1)

def main():
    # this is the main function that we will run, below are the acceptable inputs for a variable below
    random_options = ['y','n','yes','no']
    period, month, year = get_time_period()
    df_clean = load_data(period, month, year)

    total_search_breakdown(df_clean)
    ethnicity_breakdown(df_clean)
    objective_breakdown(df_clean)
    eth_objective_breakdown(df_clean)
    gender_breakdown(df_clean)
    age_breakdown(df_clean)
    time_series_graphs(df_clean)

    while True:
        try:
            rand_input = str(input('\nWould you like to see a random stop and search entry? (y/n) \n'))
        # if there is a value error it will print this
        except ValueError:
            print("{} was sadly not understood".format(rand_input))
        # if it is not part of the pre-defined list above it will print this
        if rand_input.lower() not in random_options:
            print("{}, was sadly not an option".format(rand_input))
            continue
        # if some determined variables are selected it will run the function to show random trips
        # this will loop until 'n' is entered
        elif rand_input.lower() == 'y' or rand_input.lower() == 'yes':
            random_line(df_clean)
            continue
        # if 'n' is chosen the script will shut down
        else:
            print("Okay, thanks for analysing some data! We will now exit. Run the script again if you want more insights.")
            raise SystemExit
            break

if __name__ == '__main__':
    main()
