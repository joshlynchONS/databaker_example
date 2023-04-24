import json
from additional_functions import load_and_create_dataframe
import pandas as pd


def run_pipeline():
    with open('multi_cat_config.json', 'r') as f:
        config = json.load(f)

    list_df = []
    for section in config["sections"]:
        df = load_and_create_dataframe(section)
        list_df.append(df)
        
    concat_df = pd.concat(list_df)
    concat_df.to_csv("databaker_format.csv")
    
    print(concat_df)

if __name__ == "__main__":
    run_pipeline()