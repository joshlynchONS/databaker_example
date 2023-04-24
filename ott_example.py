import json
from additional_functions import load_table, create_conversion_segment


def run_pipeline():
    with open('ott_example_config.json', 'r') as f:
        config = json.load(f)
        
    table = load_table(config)
    conversion_segment = create_conversion_segment(table, config)
    df = conversion_segment.topandas()

    df.to_csv("databaker_format.csv")
    print(df)
    

if __name__ == "__main__":
    run_pipeline()