import numpy as np
import pandas as pd
from pathlib import Path
import re

import os 


def treat_price(x):
    if type(x) == float:
        return x
    else:
        if x[1] == 'Lac':
            return round(float(x[0])/100,2)
        else:
            return round(float(x[0]),2)


def load_df(csv_path):
    df = pd.read_csv(csv_path)

    df.drop(columns=['link', 'property_id'], inplace=True)
    df.rename(columns={'area': 'price_per_sqft'}, inplace=True)

    df['society'] = (
        df['society']
        .apply(lambda name: re.sub(r'\d+(\.\d+)?\s?★', '', str(name)).strip())
        .str.lower()
    )
    df = df[df['price'] != 'Price on Request']
    df['price'] = df['price'].str.split(' ').apply(treat_price)
    df['price_per_sqft'] = (
        df['price_per_sqft']
        .str.split('/')
        .str.get(0)
        .str.replace('₹', '')
        .str.replace(',', '')
        .str.strip()
        .astype(float)
    )
    df = df[~df['bedRoom'].isnull()]
    df['bedRoom'] = df['bedRoom'].str.split(' ').str.get(0).astype(int)
    df['bathroom'] = df['bathroom'].str.split(' ').str.get(0).astype(int)
    df['balcony'] = df['balcony'].str.split(' ').str.get(0).str.replace('No', '0')

    # df['additionalRoom'].fillna('not available', inplace=True)
    # df['additionalRoom'] = df['additionalRoom'].str.lower()

    df['floorNum'] = (
        df['floorNum']
        .str.split(' ')
        .str.get(0)
        .replace({'Ground': '0', 'Basement': '-1', 'Lower': '0'})
        .str.extract(r'(\d+)')
        .astype(float)
    )

    df['additionalRoom'] = df['additionalRoom'].fillna('not available')
    df['additionalRoom'] = df['additionalRoom'].str.lower()
    df['facing'] = df['facing'].fillna('NA')

    df.insert(
        loc=4,
        column='area',
        value=round((df['price'] * 10000000) / df['price_per_sqft'])
    )

    return df

def main():
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    # input file
    csv_path = BASE_DIR / "data" / "raw" / "main_df" / "flats.csv"

    # output file
    output_dir = BASE_DIR / "data" / "raw" / "clean"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "flats_cleaned.csv"

    # load & process
    df = load_df(csv_path)

    # save
    df.to_csv(output_path, index=False)
    print(f"✅ Data saved to: {output_path}")

    print("working")
    # print(df['price'])




if __name__ == "__main__":
    main()
