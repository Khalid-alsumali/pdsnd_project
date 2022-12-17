import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
     Asks user to specify a city, month, and day to analyze.

     Returns:
         (str) city - name of the city to analyze
         (str) month - name of the month to filter by, or "all" to apply no month filter
         (str) day - name of the day of week to filter by, or "all" to apply no day filter
     """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    while True:
        city_input = str(input('Please enter the name of the city\n\n1-Chicago\n2-New york city\n3-Washington\n'))
        city_list = ['chicago', 'new york city', 'washington']
        if city_input.lower() in city_list:
            city = city_input.lower()
            print('Let\'s See {}!! '.format(city).capitalize())
            break
        else:
            print("\nplease enter a valid city name !!\n")

    # get user input for month (all, january, february, ... , june)
    while True:
        month_input = str(input(
            '\nPlease enter the month\n0-All            1-January\n2-Februaryn      3-March\n4-April          5-May\n6-June\n '))
        month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        if month_input.lower() in month_list:
            month = month_input.lower()
            print('You chose ', month.capitalize())
            break
        else:
            print('\nplease enter a valid number!!\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_input = str(input(
            '\nPlease choose the day\n0-All           1-Sunday\n2-Monday        3-Tuesday\n4-Wednesday     5-Thursday\n6-Friday        7-Saturday\n '))
        day_list = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        if day_input.lower() in day_list:
            day = day_input.lower()
            print('You chose ', day.capitalize())
            break
        else:
            print('\nplease enter a valid number!!\n')
    print('-' * 40)
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

    # extract month, day of week, hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month_list = ['january', 'february', 'march', 'april', 'may', 'june']
        month = month_list.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day_list = ['sunday', 'monday', ' tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        day = day_list.index(day) + 1

        # filter by day to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """
        Displays statistics on the most frequent times of travel.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most Common Month:', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most Day Of Week:', common_day)

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """
        Displays statistics on the most frequent times of travel.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most Used Start Station: ', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most Used End Station:', common_end_station)

    # display most frequent combination of start station and end station trip
    group_field = df.groupby(['Start Station', 'End Station'])
    combination_station = group_field.size().sort_values(ascending=False).head(1)
    print('Most frequent combination of Start Station and End Station trip:\n', combination_station)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """
        Displays statistics on the total and average trip duration.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """
        Displays statistics on bikeshare users.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Type:')
    print(df['User Type'].value_counts())
    if city != 'washington':
        # Display counts of gender
        print('Gender Stats:')
        print(df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        print('Birth Year:')
        most_common_year = df['Birth Year'].mode()[0]
        print('Most Common Year:', most_common_year)
        most_recent_year = df['Birth Year'].max()
        print('Recent Year:', most_recent_year)
        earliest_year = df['Birth Year'].min()
        print('Earliest Year:', earliest_year)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    check = True
    while check:
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_display = input("Do you wish to continue?: ").lower()
        if view_display == "no":
            check = False


def main():
    city, month, day = get_filters()
    df = load_data(city, month, day)

    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df, city)
    display_data(df)

    while True:
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() == 'no':
            exit(print('\nSee you soon!!\n'))
            break
        elif restart.lower() != 'yes':
            print('\nEnter a valid answer\n')
        else:
            main()


if __name__ == "__main__":
    main()
