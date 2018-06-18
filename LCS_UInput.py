import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None

#this function is to get the uder time that we will use for exploring data
def get_time_period():
    period_options = ['month', 'year', 'none']
    month_options = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    month_options_17 = ['january', 'february', 'march', 'april' ]
    year_options = [2016, 2017]

    print('\nHello, in this script you will be able to get details about London Stop and Search data!')
    print('\nFirst thing that we want to do is see what time period you want to view the data for.')
    print('\nBy default we will range from January 2016 to April 2017, but you have the option to filter the data')

    #This will ask for an input to see how the user wants to search the data. The loop merely ensures that what we select is supported.
    while True:
        try:
            period_input = str(input('\nYou can filter by month, year or not at all. If you want no filter, type "none":\n'))
        except ValueError:
            print('{} was sadly not understood'.format(period_input))
            continue
        if period_input.lower() not in period_options:
            print('Sadly {} was not an option'.format(period_input))
            continue
        else:
            period = period_input.lower()
            break
    #if the user has selected to filter on months, we need to know what months they want to filter on
    if period == 'month':
        while True:
            try:
                year_m_input = int(input('\nYou have selected to filter by month - but we need to choose year too, what do you want to choose? (remember we only have a few months for 2017)\n'))
            except ValueError:
                print('Sadly not understood, enter a year, 2016 or 2017...')
                continue
            if year_m_input not in year_options:
                print('{} that was not a year on the list, its 2016 or 2017...'.format(year_m_input))
                continue
            else:
                year = year_m_input
                break
        while True:
            try:
                month_input = str(input('\nYou have selected to filter by month - lets see what month you want to look at!'))
            except ValueError:
                print('{} was sadly not understood'.format(month_input))
                continue
            if month_input.lower() not in month_options:
                print('Apologies, {} is not actually a month....'.format(month_input))
                continue
            if year_m_input == 2017 and month_input.lower() not in month_options_17:
                print('Apologies, we do not have {} data for 2017...'.format(month_input.title()))
            else:
                month = month_input.lower()
                break
    #if the user wants to search by year, lets find out what year
    elif period == 'year':
        while True:
            try:
                year_input = int(input('\nPlease enter the year you want to search on (remember we only have a few months for 2017), what year shall we search on?'))
            except ValueError:
                print('{} that is not a legitimate thing to enter'.format(year_input))
                continue
                print('{} that was not a year on the list, its 2016 or 2017...'.format(year_input))
                continue
            else:
                year = year_input
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
    df = pd.read_csv('Data/london-stop-and-search.csv', low_memory=False)

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

    print('\nThe below table shows the count of total stop and search by month')

    date_to_month = df_clean.date.dt.to_period("M")
    date_group = df_clean.groupby(date_to_month)
    print(date_group['date'].count())

    plot_options = ['y', 'n']
    while True:
        try:
            tsb_input = str(input('\nDo you want to see this in graph format? (y/n)'))
        except ValueError:
            print('{} was not a legit input, needs to be a string'.format(tsb_input))
            continue
        if tsb_input.lower() not in plot_options:
            print('{} was not a valid input, needs to be "y" or "n"'.format(tsb_input))
            continue
        if tsb_input.lower() == 'y':
            plt.figure(figsize=(10,7))
            plt.xlabel('Date')
            plt.ylabel('Count of Stop and Search Record')
            plt.title('Time series graph showing stop and search activity')
            plt.plot(count_by_date)
            plt.show()
            break
        else:
            print('Okay not a problem - the graph will not be shown')
            break

def ethnicity_breakdown(df_clean):
    print('\nThe below table shows the count of stop and search by ethnicity')

    print(df_clean['ethnicity'].value_counts())

    plot_options = ['y', 'n']
    while True:
        try:
            eb_input = str(input('\nDo you want to see this in graph format? (y/n)'))
        except ValueError:
            print('{} was not a legit input, needs to be a string'.format(eb_input))
            continue
        if eb_input.lower() not in plot_options:
            print('{} was not a valid input, needs to be "y" or "n"'.format(eb_input))
            continue
        if eb_input.lower() == 'y':
            df_clean['ethnicity'].value_counts().plot.bar(title='stop_and_search_by_ethnicity',figsize=(10,7))
            plt.show()
            break
        else:
            print('Okay not a problem - the graph will not be shown')
            break

def objective_breakdown(df_clean):
    print('\nThe below table shoes the count of stop and search by objective')

    print(df_clean['object_of_search'].value_counts())

    plot_options = ['y', 'n']
    while True:
        try:
            ob_input = str(input('\nDo you want to see this in graph format? (y/n)'))
        except ValueError:
            print('{} was not a legit input, needs to be a string'.format(ob_input))
            continue
        if ob_input.lower() not in plot_options:
            print('{} was not a valid input, needs to be "y" or "n"'.format(ob_input))
            continue
        if ob_input.lower() == 'y':
            df_clean['object_of_search'].value_counts().plot.bar(title='Stop and Search by Object of Search',figsize=(10,7))
                df_clean['object_of_search'].value_counts().plot.bar(title='Stop and Search by Object of Search',figsize=(10,7))
            plt.show()
            break
        else:
            print('Okay not a problem - the graph will not be shown')
            break

    print('\nThe below groups "Controlled Drugs" and "Articles for use in Criminal Damage" and shows them as a percentage of each other')
    counts = df_clean['object_of_search'].value_counts()
    counts[counts > 5000]

    #creating some masks for the two we are ooking for
    drugs = df_clean.object_of_search == 'Controlled drugs'
    criminal_damage = df_clean.object_of_search == 'Articles for use in criminal damage'

    #creating a total that we can use as denominator for the percentage calculator
    drugs_p_crimdam = df_clean.object_of_search[drugs].count() + df_clean.object_of_search[criminal_damage].count()

    #creating some percentages for the pie chart
    drugs_prc = df_clean.object_of_search[drugs].count() / drugs_p_crimdam
    criminal_damage_prc = df_clean.object_of_search[criminal_damage].count() / drugs_p_crimdam

    print('Percentage that is drugs: ' + str(drugs_prc))
    print('Percentage that is Criminal Damage: ' + str(criminal_damage_prc))

    plot_options = ['y', 'n']
    while True:
        try:
            ob2_input = str(input('\nDo you want to see this? (in graph format) (y/n)'))
        except ValueError:
            print('{} was not a legit input, needs to be a string'.format(ob2_input))
            continue
        if ob2_input.lower() not in plot_options:
            print('{} was not a valid input, needs to be "y" or "n"'.format(ob2_input))
            continue
        if ob2_input.lower() == 'y':
            # this will plot a pie chart for us using the above
            labels = 'Controlled Drugs', 'Articles for use in criminal damage'
            fracs = [drugs_prc, criminal_damage_prc]
            explode = (0,0)
            plt.axis("equal")
            plt.title('Percentage Drug vs. Weapons search as pct of Drugs plus Weapons')
            plt.pie(fracs, explode=explode, labels=labels, autopct='%.0f%%', shadow=True)
            plt.show()
            break
        else:
            print('Okay not a problem - the graph will not be shown')
            break

def eth_objective_breakdown(df_clean):
    print('\nThe below groups ethnicity and obective breakdowns together to try and show us some trends')

    print('\nHere is a table by objective of search and then by ethnicity')
    print(df_clean.groupby('ethnicity')['object_of_search'].value_counts().unstack(0))

    plot_options = ['y', 'n']
    while True:
        try:
            eob_input = str(input('\nDo you want to see this? (in graph format) (y/n)'))
        except ValueError:
            print('{} was not a legit input, needs to be a string'.format(eob_input))
            continue
        if eob_input.lower() not in plot_options:
            print('{} was not a valid input, needs to be "y" or "n"'.format(eob_input))
            continue
        if eob_input.lower() == 'y':
            df_clean.groupby('ethnicity')['object_of_search'].value_counts().unstack(0).plot.bar(title='Object of search by Ethnicity', figsize=(10,7))
            plt.show()
            break
        else:
            print('Okay not a problem - the graph will not be shown')
            break

    plot_options = ['y', 'n']
    while True:
        try:
            eob2_input = str(input('\nDo you want to see a graph that maps by ethnicity and then objective of search? (in graph format) (y/n)'))
        except ValueError:
            print('{} was not a legit input, needs to be a string'.format(eob2_input))
            continue
        if eob2_input.lower() not in plot_options:
            print('{} was not a valid input, needs to be "y" or "n"'.format(eob2_input))
            continue
        if eob2_input.lower() == 'y':
            df_clean.groupby('object_of_search')['ethnicity'].value_counts().unstack(0).plot.bar(title='Ethnicity by Object of Search', figsize=(10,7))
            plt.show()
            break
        else:
            print('Okay not a problem - the graph will not be shown')
            break

def gender_breakdown(df_clean):
    print('\nThis here will show us a table of Gender by the Objective of search')

    print(df_clean.groupby('gender')['object_of_search'].value_counts().unstack(0))

    plot_options = ['y', 'n']
    while True:
        try:
            gb_input = str(input('\nDo you want to see this? (in graph format) (y/n)'))
        except ValueError:
            print('{} was not a legit input, needs to be a string'.format(gb_input))
            continue
        if gb_input.lower() not in plot_options:
            print('{} was not a valid input, needs to be "y" or "n"'.format(gb_input))
            continue
        if gb_input.lower() == 'y':
            df_clean.groupby('object_of_search')['gender'].value_counts().unstack(0).plot.bar(title='Gender by Object of Search', figsize=(10,7));
            plt.show()
            break
        else:
            print('Okay not a problem - the graph will not be shown')
            break

    print('\nNow lets see that total stop and search counts by Gender as a percentage of total')

    #creating some masks
    gender_male = df_clean.gender == 'Male'
    gender_female = df_clean.gender == 'Female'
    gender_other = df_clean.gender == 'Other'

    #creating percentages
    gender_male_prc = df_clean.gender[gender_male].count() / len(df_clean)
    gender_female_prc = df_clean.gender[gender_female].count() / len(df_clean)
    gender_other_prc = df_clean.gender[gender_other].count() / len(df_clean)

    print('Percentage that is male: ' + str(gender_male_prc))
    print('Percentage that is female: ' + str(gender_female_prc))
    print('Percentage that is other: ' + str(gender_other_prc))

    plot_options = ['y', 'n']
    while True:
        try:
            gb2_input = str(input('\nDo you want to see a this? (in graph format) (y/n)'))
        except ValueError:
            print('{} was not a legit input, needs to be a string'.format(gb2_input))
            continue
        if gb2_input.lower() not in plot_options:
            print('{} was not a valid input, needs to be "y" or "n"'.format(gb2_input))
            continue
        if gb2_input.lower() == 'y':
            # this will plot a pie chart for us using the calcs above
            labels = 'Male', 'Female', 'Other'
            fracs = [gender_male_prc, gender_female_prc, gender_other_prc]
            explode = (0.0,0,0)
            plt.axis("equal")
            plt.title('Percentage of Stop and Search by Gender')
            plt.pie(fracs, explode=explode, labels=labels, autopct='%.0f%%', shadow=True)
            plt.show()
            break
        else:
            print('Okay not a problem - the graph will not be shown')
            break

def age_breakdown(df_clean):
    print('\nNow lets see an age breakdown by count as percentage of total')

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

    print('Percentage that is under 10: ' + str(age_u10_prc))
    print('Percentage that is 10-17: ' + str(age_10_prc))
    print('Percentage that is 18-24: ' + str(age_18_prc))
    print('Percentage that is 25-34: ' + str(age_25_prc))
    print('Percentage that is 35+: ' + str(age_34_prc))

    plot_options = ['y', 'n']
    while True:
        try:
            ab_input = str(input('\nDo you want to see this? (in graph format) (y/n)'))
        except ValueError:
            print('{} was not a legit input, needs to be a string'.format(ab_input))
            continue
        if ab_input.lower() not in plot_options:
            print('{} was not a valid input, needs to be "y" or "n"'.format(ab_input))
            continue
        if ab_input.lower() == 'y':
             # and a pie chart
            labels = 'Under 10', '10-17', '18-24', '25-34', '35+'
            fracs = [age_u10_prc, age_10_prc, age_18_prc, age_25_prc, age_34_prc]
            explode = (0,0,0,0,0)
            plt.axis("equal")
            plt.title('Percentage of Stop and Search by Age range')
            plt.pie(fracs, explode=explode, labels=labels, autopct='%.0f%%', shadow=True)
            plt.show()
            break
        else:
            print('Okay not a problem - the graph will not be shown')
            break

    print('\nNow lets analyse this more by looking at age by Objective of search')
    print(df_clean.groupby('age_range')['object_of_search'].value_counts().unstack(0))

    plot_options = ['y', 'n']
    while True:
        try:
            ab2_input = str(input('\nDo you want to see this? (in graph format) (y/n)'))
        except ValueError:
            print('{} was not a legit input, needs to be a string'.format(ab2_input))
            continue
        if ab2_input.lower() not in plot_options:
            print('{} was not a valid input, needs to be "y" or "n"'.format(ab2_input))
            continue
        if ab2_input.lower() == 'y':
            df_clean.groupby('object_of_search')['age_range'].value_counts().unstack(0).plot.bar(title='Age range by Object of Search', figsize=(10,7))
            plt.show()
            break
        else:
            print('Okay not a problem - the graph will not be shown')
            break

def time_series_graphs(df_clean):
    print('\nWe have looked at top level statistics now, but what is useful is to see how things change over time')
    print('\nFor that lets plot some graphs showing change over time')

    plot_options = ['y', 'n']
    while True:
        try:
            ts_input = str(input('\nLets first look at ethnicity - do you want to see this? (in graph format) (y/n)'))
        except ValueError:
            print('{} was not a legit input, needs to be a string'.format(ts_input))
            continue
        if ts_input.lower() not in plot_options:
            print('{} was not a valid input, needs to be "y" or "n"'.format(ts_input))
            continue
        if ts_input.lower() == 'y':
            #All of the below are just printing time series graphs based on data that is given
            race_count = df_clean.groupby('date')
            race_count = race_count.ethnicity.apply(pd.value_counts).unstack(-1).fillna(0)
            race_count.plot(kind='line',figsize=(10,7), title='Stop and Search Count by Race')
            plt.show()
            break
        else:
            print('Okay not a problem - the graph will not be shown')
            break

    plot_options = ['y', 'n']
    while True:
        try:
            ts2_input = str(input('\nNext lets see by objective of search - do you want to see this? (in graph format) (y/n)'))
        except ValueError:
            print('{} was not a legit input, needs to be a string').format(ts2_input)
            continue
        if ts2_input.lower() not in plot_options:
            print('{} was not a valid input, needs to be "y" or "n"'.format(ts2_input))
            continue
        if ts2_input.lower() == 'y':
            object_count = df_clean.groupby('date')
            object_count = object_count.object_of_search.apply(pd.value_counts).unstack(-1).fillna(0)
            object_count.plot(kind='line',figsize=(10,7), title='Stop and Search Count by Object of Search')
            plt.show()
            break
        else:
            print('Okay not a problem - the graph will not be shown')
            break

    plot_options = ['y', 'n']
    while True:
        try:
            ts3_input = str(input('\nNow by Gender - do you want to see this? (in graph format) (y/n)'))
        except ValueError:
            print('{} was not a legit input, needs to be a string'.format(ts3_input))
            continue
        if ts3_input.lower() not in plot_options:
            print('{} was not a valid input, needs to be "y" or "n"'.format(ts3_input))
            continue
        if ts3_input.lower() == 'y':
            gender_count = df_clean.groupby('date')
            gender_count = gender_count.gender.apply(pd.value_counts).unstack(-1).fillna(0)
            gender_count.plot(kind='line',figsize=(10,7), title='Stop and Search Count by Gender')
            plt.show()
            break
        else:
            print('Okay not a problem - the graph will not be shown')
            break

    plot_options = ['y', 'n']
    while True:
        try:
            ts4_input = str(input('\nLastly by Age - do you want to see this? (in graph format) (y/n)'))
        except ValueError:
            print('{} was not a legit input, needs to be a string'.format(ts4_input))
            continue
        if ts4_input.lower() not in plot_options:
            print('{} was not a valid input, needs to be "y" or "n"'.format(ts4_input))
            continue
        if ts4_input.lower() == 'y':
            age_count = df_clean.groupby('date')
            age_count = age_count.age_range.apply(pd.value_counts).unstack(-1).fillna(0)
            age_count.plot(kind='line', figsize=(10,7), title='Stop and Search Count by Age')
            plt.show()
            break
        else:
            print('Okay not a problem - the graph will not be shown')
            break

def random_line(df_clean):
    # this is used to select a random line of data to look at
    df_1 = df_clean.sample(n=1)
    print(df_1)

def main():
    # this is the main function that we will run, below are the acceptable inputs for a variable below
    random_options = ['y','n','yes','no']
    period, month, year = get_time_period()
    df_clean = load_data(period, month, year)

    #this will show the breakdowns based upon the user selected inputs called above.
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
            print('{} was sadly not understood'.format(rand_input))
        # if it is not part of the pre-defined list above it will print this
        if rand_input.lower() not in random_options:
            print('{}, was sadly not an option'.format(rand_input))
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

#this is the input that will run the the main funtion which kicks off the script
if __name__ == '__main__':
    main()
