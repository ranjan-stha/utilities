import pandas
import sys

# Format of the command:
# python python_file_name.py MainCSVFileName.csv CurrentCSVFileName.csv MAIN_FILE_COL_NAME CURRENT_FILE_COL_NAME NEW_ADDED_COL_NAME

'''
This script automates the attendance keeping of the students by integrating the current attendance records into the main attendance file.

Created on: 27 August 2020
Created by: Ranjan Shrestha, ranjan.shrestha.np@gmail.com

Program bugs should be directed to ranjan(dot)shrestha(dot)np(at)gmail(dot)com

'''

__author__ = 'ranjan-stha'

print (f"Number of arguments: {len(sys.argv)}")
print (f"Argument list: {str(sys.argv)}")

if len(sys.argv) != 6:
	print ("Not enough arguments !! Five arguments should be passed.")
	print ("Exiting!!")
	sys.exit(0)

# Argument Parsing
MAIN_FILE = sys.argv[1]
CURRENT_FILE = sys.argv[2]
MAIN_COL_NAME = sys.argv[3]
CURRENT_COL_NAME = sys.argv[4]
NEW_COL = sys.argv[5]

# Cleans the string by stripping and removing trailing spaces
def clean_string(x):
	x.strip()
	x.replace(" ", "")
	return " ".join(x.split())

# Search in the substring for a match
def search_string(x):
	for current_name in current_names.values:
		if current_name.split()[0] in x and current_name.split()[-1] in x:
			return True
	return False

# Reading the main csv file
df_main = pandas.read_csv(MAIN_FILE, sep=';|,', engine='python')
# Reading the current csv file
df_current = pandas.read_csv(CURRENT_FILE, sep=';|,', engine='python')

current_names = df_current[CURRENT_COL_NAME].str.lower().map(clean_string)
processed_current_data_1 = list(df_main[MAIN_COL_NAME].str.lower().map(clean_string).map(search_string))

processed_current_data_2 =  list(df_main[MAIN_COL_NAME].str.lower().map(clean_string).isin(df_current[CURRENT_COL_NAME].str.lower().map(clean_string)).values)

final_processed_data = processed_current_data_1 or processed_current_data_2

# Add a new column to the main dataframe
df_main[NEW_COL] = ['P' if x else 'A' for x in final_processed_data]

print ('='*50)
# Displaying the final result in main dataframe (MAX=100 records)
print (df_main.head(100))

# Store the dataframe to the main csv file
df_main.to_csv(MAIN_FILE, index=False, header=True, sep=';')
