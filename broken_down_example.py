# Load in the functions
from databaker.framework import *
import pandas as pd

# Load the spreadsheet
tabs = loadxlstabs("internetusers2020.xlsx")

# Select the second table
tab = tabs[1]

# Select the cells contatining column headers
column_headers = tab.excel_ref('C4:J4')

# Select the cells contatining row headers
row_headers = tab.excel_ref('A9:A15')

# Specify the different categories
dimensions = [ 
    HDim(tab.excel_ref('C3'), "Used", CLOSEST, ABOVE), 
    HDim(column_headers, "Years", DIRECTLY, ABOVE), 
    HDim(row_headers, "Age", DIRECTLY, LEFT)
]

# Group the obseravtions/data from your table
observations = tab.excel_ref('C9:J15').is_not_blank().is_not_whitespace()

# Necessary step before turning to a pandas df
c1 = ConversionSegment(observations, dimensions)

# Turn conversionsegment into pandas df
df = c1.topandas()
print(df)

# Beginings of the process to turn data back into a table format #
# Find unique column and row headers
unique_age = df['Age'].unique()
unique_years = df['Years'].unique()

# Create array of observations
obs = df['OBS'].to_numpy()

# Reshape observations to match original data
rearrange_obs = obs.reshape((len(unique_age), len(unique_years)))

# Create a dictionary matching row headers to their respective data
dict_obs = {}
for i in range(len(rearrange_obs)):
    dict_obs[unique_age[i]] = rearrange_obs[i]

# Create a pandas df in the same shape as the original data
new_df = pd.DataFrame.from_dict(dict_obs, orient='index', columns=unique_years)

print(new_df)
