# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 09:59:33 2020

@author: Dirk Mueller
"""
import pandas as pd
import os
from os import path
import time

# Data file names that are used by load_data() and basic_info():
fn_chicago = path.expanduser(r'C:\Users\Dirk2\Documents\chicago_t.csv')
fn_washington = path.expanduser(r'C:\Users\Dirk2\Documents\washington_t.csv')
fn_NYC = path.expanduser(r'C:\Users\Dirk2\Documents\new_york_city_t.csv')

# Dictionary to map the file names to city names:
CITY_DATA = {'chicago': fn_chicago,
             'new york city': fn_NYC,
             'washington': fn_washington}

# Dictionaries to map the input abbreviations to city, month and weekday:
CITIES = {'c': 'chicago', 'n': 'new york city', 'w': 'washington'}
M_DICT = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6}
D_DICT = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6}

SEC_IN_MIN = 60
SEC_IN_H = 3600
STEP_VALUE = 5

def load_data(city, month, day):
    """ Function to load the csv files and convert the Start Time and
        End Time into datetime objects.
        INPUT: city, month and weekday
        OUTPUT: DataFrame with the converted time columns
    """
    if city == 'c':
        file_to_open = CITY_DATA['chicago']
    elif city == 'n':
        file_to_open = CITY_DATA['new york city']
    else:
        file_to_open = CITY_DATA['washington']
    df = pd.DataFrame()
    print('File path and name:', file_to_open, '\n')
    print('Data types for ', CITIES[city].title().upper(), ':')
    if os.path.exists(file_to_open):
        df = pd.read_csv(file_to_open)
        # Conversion of date string to datetime object:
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])
        # Create new columns to for filtering the data set:
        df['month'] = df['Start Time'].dt.month
        df['day'] = df['Start Time'].dt.weekday
        df['hour'] = df['Start Time'].dt.hour
        # Reduce DataFrame to only include lines belonging to a given month:
        if month != 'non':
            df = df[df.month == M_DICT[month]]
        # Reduce DataFrame to only include lines belonging to a given weekday:
        if day != 'non':
            df = df[df.day == D_DICT[day]]
        if df.empty:
            print("There is no data fulfilling the condition.")
    else:
        print('The file does not exist or could not be read!')
    temp = 'Amount of missing values for each column: \n'
    if city in ['c', 'n']:
        print(df.iloc[:, 0:9].dtypes, '\n')
        print(temp, df.iloc[:, 0:9].isnull().sum())
    else:
        print(df.iloc[:, 0:7].dtypes, '\n')
        print(temp, df.iloc[:, 0:7].isnull().sum())
    return df

def get_5_lines_from_filter(df, city):
    """ Function to print out raw data in steps of 5 rows each
        INPUT: DataFrame of the csv file selected by the user
    """
    print('Let\'s explore its bikeshare data with these criteria:')
    if city in ['c', 'n']:
        print(df.iloc[0:6, 0:9], '\n')
    else:
        print(df.iloc[0:6, 0:7], '\n')
    if len(df.iloc[:6, :]) < 5:
        return
    cont_print = input('Would you like the next 5 (yes, no)?\n')
    if cont_print.lower() != 'yes':
        return
    start_index = 6
    while True:
        # if-else block to avoid the printing of month, day, hour columns:
        if city in ['c', 'n']:
            print(df.iloc[start_index:start_index + STEP_VALUE, 0:9])
        else:
            print(df.iloc[start_index:start_index + STEP_VALUE, 0:7])
        # if-else block to continue with printing if previous had 5 lines:
        if len(df.iloc[start_index:start_index + STEP_VALUE, :]) == 5:
            cont_print = input('\nPrint the next 5 lines (yes, no)?\n')
            if cont_print.lower() != 'yes':
                return
        else:
            break
        start_index += 5

def most_popular(df):
    ''' Function to print the:
        - most common  month, weekday, hour of the day
        - most common start and end station
        - most frequent combination of start and end station
        - count of each user type
        INPUT: DataFrame of the csv file selected by the user
    '''
    # Determine those attributes that occur most often:
    pop_month = df['month'].mode()[0]
    pop_day = df['day'].mode()[0]
    pop_hour = df['hour'].mode()[0]
    pop_start = df['Start Station'].mode()[0]
    pop_end = df['End Station'].mode()[0]
    print('*' * 64)
    print('\nMost common times for rental acc. to Start Station: ')
    keys = list(D_DICT.keys())
    vals = list(D_DICT.values())
    print('month:', pop_month, ', weekday:', pop_day, '(',
          keys[vals.index(pop_day)], '), hour:', pop_hour)
    # Determine the occurrence of pairs of Start and End Station:
    counts = df.groupby(['Start Station', 'End Station']).size()
    counts = counts.sort_values(ascending=False)
    print('\nMost common rental stations: ')
    print('Start Station: ', pop_start, '\nEnd Station: ', pop_end)
    print('\nHow many times combinations of Start and End station occurred:')
    print('counts: ', counts)
    # Determine the pair of Start and End Station that occurs most often:
    pop_comb = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('\nMost common combination of Start and End Station for rental: ')
    print(pop_comb)
    user_type = df.groupby(['User Type']).size()
    nans_type = df['User Type'].isnull().sum()
    print('\n', user_type)
    print('Empty data fields in User Type column: ', nans_type, '\n')

def trip_duration(df):
    ''' Function to print the:
        - total travel time in minutes
        - average travel time in minutes
        INPUT: DataFrame of the csv file selected by the user
    '''
    total_travel_time = df['Trip Duration'].sum()
    ave_travel_time = df['Trip Duration'].mean()
    print('Total rental time (s): ', total_travel_time)
    print('Total rental time (h): ', round(total_travel_time / SEC_IN_H, 3))
    print('Mean rental time (s): ', round((ave_travel_time), 3))
    print('Mean rental time (min): ', round(ave_travel_time / SEC_IN_MIN, 3))

def user_info(df):
    ''' Function to print the:
        - count of each gender in the NYC and Chicago data sets
        - count of each year of birth in the NYC and Chicago data sets
        INPUT: DataFrame of the csv file selected by the user
    '''
    # Determine distribution of gender:
    print(df.groupby(['Gender']).size())
    nans_gender = df['Gender'].isnull().sum()
    print('Empty data fields in Gender column: ', nans_gender, '\n')
    # Before casting the year of birth to integer the NaN's have to be droped:
    df = df.dropna(subset=['Birth Year'])
    df = df.dropna(subset=['Gender'])
    # Cast the year of birth to integer
    df['Birth Year'] = df['Birth Year'].astype(int)
    # Determine distribution of year of birth:
    print(df.groupby(['Birth Year']).size())
    print('Earliest year of birth: ', df['Birth Year'].min())
    print('Most recent year of birth: ', df['Birth Year'].max())
    print('Most common year of birth: ', df['Birth Year'].mode()[0])

def get_filters():
    ''' Function to capture the user selections with regard to filters in:
        - city, month and weekday
        OUTPUT: city, month and weekday
    '''
    temp = '\nIn the next step you can investigate data from any '
    temp += 'any of the the three cities with defined criteria for month/day.'
    print(temp)
    text_cit = 'Select a city by typing one of the following three characters'
    text_cit += ' (c: Chicago, n: New York City, w: Washington): '
    text_month = 'Select a month (jan: January, feb: February, mar = March,\
 apr: April, may: May, jun: June, or non: None)?:'
    text_day = 'Select a day (mon: Monday, tue: Tuesday, wed: Wednesday,\
 thu: Thursday, fri: Friday, sat: Saturday, sun: Sunday, or non: None): '
    while True:
        city = input(text_cit)
        if city.lower() in CITIES.keys():
            break
        else:
            print('No such city. Please try again!')
    while True:
        month = input(text_month)
        if (month.lower() in M_DICT.keys()) or (month.lower() == 'non'):
            break
        else:
            print('Your input had neither month, nor none. Please try again!')
    while True:
        day = input(text_day)
        if (day.lower() in D_DICT.keys()) or (day.lower() == 'non'):
            break
        else:
            print('Your input had neither weekday nor none. Please try again!')
    return city, month, day

def basic_info():
    ''' Function that displays the basic information of the csv files:
        - file size in KB
        - time needed to load the csv file into memory
        - Amount of data rows in csv file
        - Amount of missing values for each column
    '''
    for item in CITY_DATA:
        print('\n')
        print('*' * 64)
        temp = 'Basic properties of Bikeshare csv file for'
        print(temp, item.title().upper(), ':')
        # Check if file exists:
        if os.path.exists(CITY_DATA[item]):
            file_size_KB = round(path.getsize(CITY_DATA[item]) / (1 << 10), 1)
            print('Size: ', file_size_KB, 'KB')
            # Measure time to load the file:
            t0 = time.time()
            df = pd.read_csv(CITY_DATA[item])
            t1 = time.time() - t0
            print('Time for loading the csv file:', round(t1, 5), 's')
            print('Amount of rows:', len(df))
            print('\nThe table has the following columns and types:')
            print(df.dtypes, '\n')
            if (item == 'new york city') or (item == 'chicago'):
                print(df[['Trip Duration', 'Birth Year']].describe(), '\n')
            else:
                print(df[['Trip Duration']].describe(), '\n')
            temp = 'Amount of unique'
            print(temp, 'Start Stations:', df['Start Station'].nunique())
            print(temp, 'End Stations:', df['End Station'].nunique())
        else:
            print('The file does not exist!')

def main():
    print('*' * 64)
    print('Project 2: NanoDegree \'Programming for Data Science with Python\'')
    print('Dirk Mueller, 2020-10-13')
    print('*' * 64)
    temp = 'Do you want to see the basic info of all 3 csv files? '
    temp = temp + 'Note: this involves pre-loading of the csv files!'
    temp = temp + ' Type y for yes: '
    see_basic_info = input(temp)
    if see_basic_info == 'y':
        basic_info()
    while True:
        print('*' * 64)
        # Get user input and return as tuple:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        # if df.empty:
        #     sys.exit("Because of the error the program has to be aborted.")
        # else:
        if not df.empty:
            print('*' * 64)
            print(CITIES[city].title().upper(), '(month: ', month,
                  ', weekday: ', day, ')')
            get_5_lines_from_filter(df, city)
            most_popular(df)
            trip_duration(df)
            # If city was not Washington analysis is continued for NYC and C.:
            if (city == 'n') or (city == 'c'):
                user_info(df)
            cont = input('Do you want to restart (y/n)?')
            if cont != 'y':
                break
        else:
            print('\nThe DataFrame is empty, no rows to work with. Try again!')


if __name__ == "__main__":
    main()
