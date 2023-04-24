import json
from additional_functions import reshape_dataframe, load_and_create_dataframe


def run_pipeline():
    with open('example_config.json', 'r') as f:
        config = json.load(f)

    df = load_and_create_dataframe(config)
    df.to_csv("databaker_format.csv")
    
    print(df)

if __name__ == "__main__":
    run_pipeline()