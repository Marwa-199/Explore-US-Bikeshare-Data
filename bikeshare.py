import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def check_data(input_str,input_type):
    """
    check the validity of user input.
    input_str: is the input of the user
    input_type: is the type of input: 1 = city, 2 = month, 3 = day
    """
    while True:
        input_read=input(input_str)
        try:
            if   input_read.lower() in ['chicago','new york city','washington'] and input_type == 1:
                break
            elif input_read.lower() in ['january', 'february', 'march', 'april', 'may', 'june','all'] and input_type == 2:
                break
            elif input_read.lower() in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all'] and input_type == 3:
                break

            else:
                if input_type == 1:
                    print("Sorry, your input should be: Chicago, New York City or Washington")
                if input_type == 2:
                    print("Sorry, your input should be: january, February ... June or All")
                if input_type == 3:
                    print("Sorry, your input should be: Monday, Tuesday ... Sunday or All")
     
        except ValueError:
            print("Sorry, Please provide a valid input from the list")
    return input_read
            
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    
    print('Hello! Let\'s explore some US bikeshare data!') 
    
    city = check_data("Which city would you like to choose and view its data ? (Chicago, New York City or Washington) ",1)
    month= check_data("Which month would you like to view ? (January, February, March, April, May, June or all) ", 2)
    day  = check_data("Which day would you like to view ? ( Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all)", 3)
    
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour   
    
    if month != 'all':      
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]


    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    # display the most common month
    # display the most common day of week
    # display the most common start hour
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
        
    df['month'] = df['Start Time'].dt.month
    Popular_Month = df['month'].mode()[0]
    print("The Most Popular month :", Popular_Month )

    df['weekday'] = df['Start Time'].dt.weekday_name
    Popular_Weekday = df['weekday'].mode()[0] 
    print("The Most Popular Day Of The Week :", Popular_Weekday )	

    df['hour'] = df['Start Time'].dt.hour
    Popular_Hour = df['hour'].mode()[0]
    print("Most Popular Start Hour :", Popular_Hour)        
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    # display most commonly used start station
    # display most commonly used end station
    # display most frequent combination of start station and end station trip
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    Common_start_Station= df['Start Station'].mode()[0]
    print("Common start Station :", Common_start_Station )
    
    Common_End_Station= df['End Station'].mode()[0]
    print("Common End Station :",Common_End_Station)
   
    Freq_comb_station=df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).head(1)
    print("Most frequent combination of "+"\n",Freq_comb_station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    # display total travel time
    # display mean travel time
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    Total_trvl_time =  df['Trip Duration'].sum() 
    print("Total travel time :", int(Total_trvl_time/3600) ,'hours and',int((Total_trvl_time%3600)/60),"minutes") 
    Average_trvl_Time =  df['Trip Duration'].mean()
    print("Average travel time :", Average_trvl_Time/60,"minutes" )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df,city):
    """Displays statistics on bikeshare users."""
    # Display counts of user types
    # Display counts of gender
    # Display earliest, most recent, and most common year of birth

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    User_types = df['User Type'].value_counts()
    print("User types Stats :"+"\n",User_types)    
        
    if city != 'washington':
        Gender_types = df['Gender'].value_counts()
        print("Gender types Stats:"+"\n",Gender_types)
        Earliest_Year=df['Birth Year'].min() 
        print("The Earliest Birth Year :",int(Earliest_Year))
        Common_Year= df['Birth Year'].mode()[0]
        print("The Most Common Birth Year :",int(Common_Year))
        Recent_Year=df['Birth Year'].max()
        print("The Most Recent Birth Year :",int(Recent_Year))
    else:
        print("Unfortunately, Gender and Birth Year Stats are not available for Washington ")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_trip_data(df,city):
    """
    Asks user if they want to view 5 lines of the trip data.
    Returns the 5 lines of raw data if user inputs `yes`,repeat until the user response is `no`
    """
    rows = 0
    while True:
        answer = input('Would you like to view trip data ?  ( Yes or No ) ')

        if answer.lower() == 'yes':
             if city == 'washington':
                print(df.iloc[ rows:rows+5 , : 7 ])
                rows += 5
             else:
                print(df.iloc[ rows:rows+5 , : 9 ])
                rows += 5
        else:
             break
            
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_trip_data(df,city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
