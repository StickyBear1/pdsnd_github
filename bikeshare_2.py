import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_LIST = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
DAY_LIST = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        city = input("Enter the city you want to explore: ").lower()
        if city not in CITY_DATA.keys(): #checks if city is valid against CITY_DATA
            print("Sorry, please enter Chicago, New York City, or Washington only")
            continue
        else:
            #user entered a city from CITY_LIST, we can break out now
            break

    while True:
        month = input("Enter the month you want to explore: ").lower()
        if month not in MONTH_LIST: #checks if month not in MONTH_LIST
            print("Sorry, please enter January, February, March, April, May, June, or All")
            continue
        else:
            #user entered a month from month_list, we can break out now
            break

    while True:
        day = input("Enter the day of the week you want to explore: ").lower()
        if day not in DAY_LIST: #checks if day not in DAY_LIST
            print("Sorry, please enter Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All")
            continue
        else:
            #user entered a valid day of week, we can break out now
            break

    print('-'*40)
    return city, month, day


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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


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
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    if month != 'all': #finds most popular month if no month is specified
        print('No mode available when month is specified.')
    else:
        df['Month'] = df['Start Time'].dt.month
        popular_month = df['Month'].mode()[0]
        print('Most common month (january = 1...): ', popular_month)

    if day != 'all': #finds most popular day if not day is specified
        print('No mode available when day is specified.')
    else:
        df['Day'] = df['Start Time'].dt.weekday
        popular_day = df['Day'].mode()[0]
        print('Most common day (monday = 0, sunday = 6: ', popular_day)

        #finds most popular hour
    df['Start Hour'] = df['Start Time'].dt.hour
    popular_hour = df['Start Hour'].mode()[0]
    print('Most common start hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #finds most popular start
    popular_start = df['Start Station'].mode()[0]
    print('The most popular start station is: ', popular_start)

    #finds most popular end
    popular_end = df['End Station'].mode()[0]
    print('The most popular end station is: ', popular_end)

    #finds most popular start and end combination
    df['Start and End'] = df['Start Station'] + df['End Station']
    popular_combo = df['Start and End'].mode()[0]
    print('The most popular start and end station combination is: ', popular_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #finds total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total seconds spent traveling is: ', total_travel_time)

    #finds average travel time
    mean_travel = df['Trip Duration'].mean()
    print('The mean seconds travelled is: ', mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #finds user types and their quantity
    user_types = df['User Type'].value_counts()
    print(user_types)

    #displays gender info if available
    if 'Gender' in df.columns:
        user_gender = df['Gender'].value_counts()
        print(user_gender)
    else:
        print('No gender information available')

    #displays oldest, earliest, and most common user birth year
    if 'Birth Year' in df.columns:
        earliest = df['Birth Year'].min()
        latest = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print('The earliest birth year is: ', int(earliest))
        print('The latest birth year is: ', int(latest))
        print('The most common birth year is: ', int(most_common))
    else:
        print('No birth year information available')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#makes raw data accessible 5 lines at a time
def raw(df):
    iloc_start = 0
    while True:
        raw_input = input('Do you want to see 5 lines of raw data? (y/n): ').lower()
        if raw_input != 'y':
            print('Okay!')
            break
        else:
            print(df.iloc[iloc_start:iloc_start+5])
            iloc_start += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
