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
    df = df.drop_duplicates()
    # Columns to drop -> property_name, link, property_id
    df.drop(columns=['link','property_id'], inplace=True)
    # rename columns
    df.rename(columns={'rate':'price_per_sqft'},inplace=True)
    
    df['society'] = df['society'].apply(lambda name: re.sub(r'\d+(\.\d+)?\s?★', '', str(name)).strip()).str.lower()
    df['society'].value_counts().shape
    df['society'] = df['society'].str.replace('nan','independent')
    # price
    df['price'].value_counts()
    df = df[df['price'] != 'Price on Request']
    df['price'] = df['price'].str.split(' ').apply(treat_price)
    # price_per_sqft
    df['price_per_sqft'].value_counts()
    df['price_per_sqft'] = df['price_per_sqft'].str.split('/').str.get(0).str.replace('₹','').str.replace(',','').str.strip().astype('float')
    # bedrooms
    df['bedRoom'].value_counts()
    df[df['bedRoom'].isnull()]
    df = df[~df['bedRoom'].isnull()]
    df['bedRoom'] = df['bedRoom'].str.split(' ').str.get(0).astype('int')
    df['balcony'] = df['balcony'].str.split(' ').str.get(0).str.replace('No','0')
    df['additionalRoom'].fillna('not available',inplace=True)
    df['additionalRoom'] = df['additionalRoom'].str.lower()
    # floors
    df['noOfFloor'].value_counts()
    df['noOfFloor'].isnull().sum()
    df['noOfFloor'] = df['noOfFloor'].str.split(' ').str.get(0)
    df.rename(columns={'noOfFloor':'floorNum'},inplace=True)
    df['additionalRoom'] = df['additionalRoom'].fillna('not available')
    df['facing'] = df['facing'].fillna('NA')

    df['area'] = round((df['price']*10000000)/df['price_per_sqft'])
    df.insert(loc=1,column='property_type',value='house')
    return df







def main():
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    # input file
    csv_path = BASE_DIR / "data" / "raw" / "main_df" / "houses.csv"

    # output file
    output_dir = BASE_DIR / "data" / "raw" / "clean_houses"
    output_dir.mkdir(parents=True, exist_ok=True)


    output_path = output_dir / "houses_cleaned.csv"

    # load & process
    df = load_df(csv_path)

    # save
    df.to_csv(output_path, index=False)
    print(f"✅ Data saved to: {output_path}")

    print("working")
    # print(df['price'])




if __name__ == "__main__":
    main()

