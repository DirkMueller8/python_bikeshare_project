## Analysis of bikeshare data from three US cities
**********************************************
Software:	&emsp;	Python 3.8.3

Version:   &emsp; 	1.0

Date: 	&emsp;		Oct 13, 2020

Author:	&emsp;		Dirk Mueller
**********************************************  

The objective of this software is to fulfill the requirements of project 2 of the Udacity's "Programming for Data Science with Python" NanoDegree (https://www.udacity.com/course/programming-for-data-science-nanodegree--nd104). It analyzes bikeshare data from three cities: New York City, Washington and Chicago.
(The original csv files contain 300.000 rows each, the test versions renamed to *_t.csv here just about a dozen rows.)

The Pandas library is used to analyze the data. Functions and dictionaries are used widely, however, no classes.

```python
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
```

*Fig 1: Excerpt of code showing the function to read and parse the data in csv format*

Example results after loading the csv and analyzing data, using `groupby()`, `size()` and `sum()`, among other:

![](https://github.com/DirkMueller8/python_bikeshare_project/blob/master/snapshot_1.png)

*Fig 2: Example of output of analysis*

The following sources have been used to solve the Bikeshare project:

**Books:**
1. Udacity course
2. Data Science with Python, by J. VanderPlas, O'Reilly Media, 2017 (German version)

**Websites:**
1. Real Python Tutorial, https://realpython.com/
2. Python documentation, https://www.python.org/doc/
