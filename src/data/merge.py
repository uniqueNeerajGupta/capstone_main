import numpy as np
import pandas as pd
from pathlib import Path
import re
import os 

def load_df(csv_path_clean_flats , csv_path_clean_houses):
    #load data 
    flats = pd.read_csv(csv_path_clean_flats )
    houses = pd.read_csv(csv_path_clean_houses)

    # concat 
    df = pd.concat([flats,houses],ignore_index=True)
    return df


def main():
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    # input file
    csv_path_clean_flats = BASE_DIR / "data" / "raw" / "clean" / "flats_cleaned.csv"
    csv_path_clean_houses = BASE_DIR / "data" / "raw" / "clean_houses" / "houses_cleaned.csv"

    # output file
    output_dir = BASE_DIR / "data" / "raw" / "merge"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "gurgaon_properties.csv"

    # load & process
    df = load_df(csv_path_clean_flats ,csv_path_clean_houses)

    # save
    df.to_csv(output_path, index=False)
    print(f"✅ Data saved to: {output_path}")

    print("working")
    # print(df['price'])




if __name__ == "__main__":
    main()






