import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    city=''
    valid_cities =['chicago','new york','washington']
    while city not in valid_cities:
        city=input('Would you like to see data for Chicago, New York or Washington?\n').lower().strip()
        if city not in valid_cities:
            print("Sorry, please enter one of the following city names:Chicago, New York, or Washington")

    # get user input for month (all, january, february, ... , june)
    month=''
    valid_months = ['all','janurary', 'february', 'march','april','may','june']
    
    while month not in valid_months : 
        month = input('Which month? Enter one of the following:janurary, feburary, march, april, may or june.\n')
        month = month.lower().strip()
        if month not in valid_months:
            print("Sorry. Please enter one of the following:janurary, feburary, march, april, may or june.\n")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day =''
    valid_days=['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    
    while day not in valid_days : 
        day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? Type All for all days\n")
        day = day.lower().strip()
        if day not in valid_days:
            print("Sorry, please type one of the following: All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday")
    print('-'*40)
    return city, month, day

#--------------------------end of def get_filters--------------------------------------------------------------#



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city],index_col=0)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day.title()] #change input day to title case 

    # calculate hour 
    df['hour']=df['Start Time'].dt.hour
    return df
#---------------------------------end of load_data-----------------------------

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is")
    print(df['month'].mode()[0])

    # display the most common day of week
    print("The most common day of week is")
    print(df['day'].mode()[0])

    # display the most common start hour
    print("The most common start hour is")
    print(df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common start station is")
    print(df['Start Station'].mode()[0])

    # display most commonly used end station
    print("The most common end station is")
    print(df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['Start-End']=df['Start Station']+df['End Station']
    print("The most common start-end station trip is")
    print(df['Start-End'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time is")
    print(df['Trip Duration'].sum())

    # display mean travel time
    print("The average travel time is")
    print(df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of User Types are: ")
    print(user_types)
    print('-'*40)
    
    # Display counts of gender
    if 'Gender' not in df.columns:
        print("No gender information available")
    else: 
        gender = df['Gender'].value_counts()
        print("Counts of Gender are: \n")
        print(gender)
    print('-'*40)
   
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df.columns:
        print("No birthday year available")
    
    else:
        print("The earliest birth year is {}".format(df['Birth Year'].min()))
        print("The most recent birth year is {}".format(df['Birth Year'].max()))
        print("The most common birth year is {}".format(df['Birth Year'].mode()))
    
        print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
if __name__ == "__main__":
	main()
