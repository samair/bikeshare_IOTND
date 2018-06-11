import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']
days =   ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
month_filter = False
day_filter = False

def validate_data(city,month,day):
    """
    Routine to validate the available data.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    Returns:
        (boolean) valid: set to true/false based on the validity of the available data.
    """

    if city in CITY_DATA:
       # found city in the city data dictionary
       # check if the month entry is valid or not
        if (month in months) or (month == "all"):
           # valid entry for month
           # check now for day_of_week
           if (day  in days) or (day == "all") :
               return True
           else:
               return False
        else:
           return False
    else:
       return False


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Bikeshare data analyser:: Welcome\n')
    loop = True
    global month_filter
    global day_filter
    month_filter = False
    day_filter = False
    while(loop):
        print("\n Analyse the data using filters if you like, supported filters \n 1.city \n 2.Month \n 3.day ")

        city = input(">>>>\"city\" must be one of chicago, new york, washington [chicago]: ").lower().strip() or "chicago"

        month = input("\n >>>>\"Month\" values could be 'january', 'february',"
        " 'march', 'april', 'may', 'june',\n or \"all\" in case you want data "
        "for all the months [all]: ").lower().strip() or "all"

        day =input("\n >>>> \"day\" values accepted are from \"monday\" to "
        "\"sunday\" \n or \"all\" in case you want data for all the months [all]: ").lower().strip() or "all"
        valid=validate_data(city,month,day)
        if valid:
            loop = False
            break;
        else:
            retry =input("\nOops...Invalid entries, try again, Enter yes or no [no]:") or "no"
            if retry.lower() != "yes":
                # user does not intend to correct input so exit
                exit()


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

    global month_filter
    global day_filter
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'] )

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        print("Setting month filter....")
        month_filter = True
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june','july','aug']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        #df = df.groupby(["month"]).get_group(month)
        df = df[df["month"] == month]

    # filter by day of week if applicable
    if day != 'all':
        day_filter = True
        # filter by day of week to create the new dataframe
        # found groupby could be used, time taken ? TODO
        #df = df.groupby(["day_of_week"]).get_group(day.title())
        df = df[df["day_of_week"] == day.title()]
    print("*"*5,"Provided data has below columns with unavailable values:")
    print(df.isnull().sum())
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    global month_filter
    global day_filter
    print('\n >>Calculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month check if filter is for month you can
    # skip
    if month_filter == True:
       print("\n >>Common month analysis skipped since Filter set for month already")
    else:
        print("\n >>Most common month used : ",months[df["month"].mode()[0]-1],
        "with number of times used those months  : ",df["month"].value_counts().max())


    # display the most common day of week
    if day_filter == True:
        print("\n >>Common day analysis skipped since Filter set for day already")
    else:
        print("\n >>Most common day used : ",df["day_of_week"].mode()[0] ,
        ", number of times used that day: ",df["day_of_week"].value_counts().max())

    # display the most common start hour
    print("\n >>Most common start hour : ",df['Start Time'].dt.hour.mode()[0], "Hours",
    ", with number of times used  : ",df['Start Time'].dt.hour.value_counts().max())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n >>Calculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    global month_filter
    print("\n >>Most common  ")
    print("\n >>Start station Used [Month filter:{}, Day Filter:{}]  : "
        .format(month_filter,day_filter),df["Start Station"].mode()[0],
        ", number of times the stations was used {}".format(df["Start Station"].value_counts().max()))


    # display most commonly used end station
    print("\n >>End Station [Month filter:{}, Day Filter:{}]  : "
        .format(month_filter,day_filter),df["End Station"].mode()[0],
        ", number of times the stations was used {}".format(df["End Station"].value_counts().max()))

    # display most frequent combination of start station and end station trip
    df1 = df.groupby(["Start Station","End Station"]).size().reset_index(name ="count")
    df2 = df1.loc[df1['count'] == df1["count"].max()]
    print("\n >>Combination of these station was traveled highest for {} times :".
    format(df2["count"].values.tolist()[0]),df2["Start Station"].values.tolist()[0],"--",df2["End Station"].values.tolist()[0],)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n >>Calculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("\n >>Total Travel time :", df["Trip Duration"].sum(), " seconds")


    # display mean travel time
    print("\n >>Mean Travel time :", df["Trip Duration"].mean(), "seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\n >>Calculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    keys = df["User Type"].value_counts().index.tolist()
    values = df["User Type"].value_counts().tolist()
    for key,value in zip(keys,values):
        print("\n >>Number of Users of Type [{}]: {}".format(key,value))


    # Display counts of gender

    if "Gender" in df.columns:
        keys = df["Gender"].value_counts().index.tolist()
        values = df["Gender"].value_counts().tolist()
        for key,value in zip(keys,values):
            print("\n >>Number of Users of Gender [{}]: {}".format(key,value))
    else:
        print("Selected city does not have Gender related data")



    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        print("\n >>Earliest year of birth: ",df["Birth Year"].min())
        print("\n >>Recent year of birth: ",df["Birth Year"].max())
        print("\n >>Most common year of birth: ",df["Birth Year"].mode()[0])
    else:
        print("Selected city does not have year of birth related data")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    """
    Routine to show raw data on user request
    """
    rownum_start = 0
    rownum_end = 5
    loop = False
    print()
    show_data =input("\n Would you like to see raw data as well ?, Enter yes or no [no]:") or "no"
    if show_data == "yes":
        loop = True
    while loop:
        print(df.iloc[rownum_start:rownum_end])
        rownum_start +=5
        rownum_end +=5
        if rownum_end > len(df.index)-1 :
            print("All data has been printed, thanks!")
            break
        continue_show =input("\n Continue printing raw data, 5 rows at a time ?, Enter yes or no [no]:") or "no"
        if continue_show != "yes":
            loop = False


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no [no].\n') or "no"
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
