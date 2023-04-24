from databaker.framework import *
import pandas as pd


def load_table(config):
    tables = loadxlstabs(config['file_path'])
    table = tables[config['table_number']]
    
    return table


def create_dimension(table, dim_title, dim_settings):
    cells = table.excel_ref(dim_settings["cell_range"]).is_not_blank().is_not_whitespace()
    search_type = getattr(databaker.framework, dim_settings["search_type"])
    direction = getattr(databaker.framework, dim_settings["direction"])
    dim = HDim(cells, dim_title, search_type, direction)
    
    if "override_cells" in dim_settings:
        for cell, new_value in dim_settings["override_cells"].items():
            dim.AddCellValueOverride(table.excel_ref(cell), new_value)
            
    if "duplicate_cells" in dim_settings:
        for cells, new_value in dim_settings["duplicate_cells"].items():
            dim.DuplicateCellValueOverride(table.excel_ref(cells), table.excel_ref(new_value))
            
    return dim


def create_conversion_segment(table, config):
    dimensions = []
    for dim_title, dim_settings in config["dimensions"].items():
        dim = create_dimension(table, dim_title, dim_settings)
        dimensions.append(dim)
        
    observations = table.excel_ref(config["observation_range"]).is_not_blank().is_not_whitespace()
    conversion_segment = ConversionSegment(observations, dimensions)
    
    return conversion_segment


def reshape_dataframe(df, config):
    unique_age = df[config["reshape_row"]].unique()
    unique_years = df[config["reshape_column"]].unique()
    obs = df['OBS'].to_numpy()
    rearrange_obs = obs.reshape((len(unique_age), len(unique_years)))

    dict_obs = {}
    for i in range(len(rearrange_obs)):
        dict_obs[unique_age[i]] = rearrange_obs[i]

    new_df = pd.DataFrame.from_dict(dict_obs, orient='index', columns=unique_years)
    
    return new_df


def load_and_create_dataframe(config):
    
    table = load_table(config)
    conversion_segment = create_conversion_segment(table, config)
    df = conversion_segment.topandas()
    
    return df
    
