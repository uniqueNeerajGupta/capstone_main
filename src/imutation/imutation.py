import numpy as np
import pandas as pd
from pathlib import Path
import re
import os 
 

def outlier(csv_path):
    df = pd.read_csv(csv_path)
    return df


def main():
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    # input file
    csv_path = BASE_DIR / "data" / "processed" / "imutation" /"gurgaon_properties_missing_value_imputation.csv"

    # output file
    output_dir = BASE_DIR / "data" / "raw" / "imputation" 
    output_dir.mkdir(parents=True, exist_ok=True)


    output_path = output_dir / "gurgaon_properties_missing_value_imputation.csv"

    # load & process
    df = outlier(csv_path)

    # save
    df.to_csv(output_path, index=False)
    print(f"✅ Data saved to: {output_path}")

    print("working")
    # print(df['price'])




if __name__ == "__main__":
    main()
