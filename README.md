## Analysis of bikeshare data from three US cities
**********************************************
Software:		Python 3.8.3

Version Number:	1.0

Date: 			Oct 13, 2020

Author:			Dirk Mueller
**********************************************
The objective of this software is to fulfill the requirements of project 2 of the "Programming for Data Science with Python" NanoDegree. It analyzes bikeshare data from three cities: New York City, Washington and Chicago.
(The original csv files contain 300.000 rows each, the test versions renamed to *_t.csv here just about a dozen rows.)

The Pandas library is used to analyze the data. Functions and dictionaries are used widely, however, no classes.

![alt text](https://github.com/DirkMueller8/python_bikeshare_project/blob/master/snapshot.png "Excerpt of code showing the function to read and parse the data in csv format")

Example after loading the csv and analyzing data, using `groupby`, `size()` and `sum()`, among other:

![alt text](https://github.com/DirkMueller8/python_bikeshare_project/blob/master/snapshot_1.png "Exampel of output of analysis")

*Sources*

The following sources have been used to solve the Bikeshare project:
**Books:**
1. Udacity course
2. Data Science with Python, by J. VanderPlas, O'Reilly Media, 2017 (German version)

**Websites:**
1. Real Python Tutorial, https://realpython.com/
2. Python documentation, https://www.python.org/doc/