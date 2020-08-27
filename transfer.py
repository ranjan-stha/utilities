import pandas
import sys

# Format of the command:
# python python_file_name.py MainCSVFileName.csv CurrentCSVFileName.csv MAIN_FILE_COL_NAME CURRENT_FILE_COL_NAME NEW_ADDED_COL_NAME

'''
This program automates the attendance keeping of the students by integrating the current attendance records into the main attendance file.

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
COL1 = sys.argv[3]
COL2 = sys.argv[4]
NEW_COL = sys.argv[5]

# Cleans the string by stripping and removing trailing spaces
def clean_string(x):
	x.strip()
	x.replace(" ", "")
	return " ".join(x.split())

# Search in the substring for a match
def search_string(x):
	for current_name in current_names.values:
		if x.startswith(current_name) or current_name.startswith(x):
			return True

	return False

# Reading the main csv file
df_main = pandas.read_csv(MAIN_FILE, sep=';')

# Reading the current csv file
df_current = pandas.read_csv(CURRENT_FILE)

#available_names = df_main[COL1].values
current_names = df_current[COL2].str.lower()

#available_names.map(clean_string)
current_names = current_names.map(clean_string)

current_data = df_main['name'].str.lower().map(search_string)

#current_data =  df_main['name'].str.lower().isin(df_current['name'].str.lower()).values

# Add a new column to the main dataframe
df_main[NEW_COL] = ['P' if x else 'A' for x in current_data]

print ('='*50)
# Displaying the final result in main dataframe (MAX=100 records)
print (df_main.head(100))

# Store the dataframe to the main csv file
df_main.to_csv(MAIN_FILE, index=False, header=True, sep=';')
