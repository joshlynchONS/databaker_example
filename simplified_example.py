# Load in the functions
from databaker.framework import *
import pandas as pd


tabs = loadxlstabs("internetusers2020.xlsx")
tab = tabs[1]

column_header_range = 'C4:J4'
row_header_range = 'A9:A15'
column_title = 'Years'
row_title = 'Age'
observation_range = 'C9:J15'


def create_conversion_segment(tab, column_header_range, row_header_range, observation_range, column_title, row_title):
    column_headers = tab.excel_ref(column_header_range)
    row_headers = tab.excel_ref(row_header_range)
    observations = tab.excel_ref(observation_range)

    dimensions = [ 
        HDim(column_headers, column_title, DIRECTLY, ABOVE), 
        HDim(row_headers, row_title, DIRECTLY, LEFT)
    ]

    conversion_segment = ConversionSegment(observations, dimensions)
    
    return conversion_segment


def reshape_dataframe(df, row_title, column_title):
    unique_age = df[row_title].unique()
    unique_years = df[column_title].unique()
    obs = df['OBS'].to_numpy()
    rearrange_obs = obs.reshape((len(unique_age), len(unique_years)))

    dict_obs = {}
    for i in range(len(rearrange_obs)):
        dict_obs[unique_age[i]] = rearrange_obs[i]

    new_df = pd.DataFrame.from_dict(dict_obs, orient='index', columns=unique_years)
    
    return new_df


conversion_segment = create_conversion_segment(tab, column_header_range, row_header_range, observation_range)
df = conversion_segment.topandas()
new_df = reshape_dataframe(row_title, column_title)

print('Databaker pandas dataframe')
print(df)
print('Reshaped dataframe')
print(new_df)
