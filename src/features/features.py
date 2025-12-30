import numpy as np
import pandas as pd
from pathlib import Path
import re
import os 

# This function extracts the Super Built up area
def get_super_built_up_area(text):
    match = re.search(r'Super Built up area (\d+\.?\d*)', text)
    if match:
        return float(match.group(1))
    return None

# This function extracts the Built Up area or Carpet area
def get_area(text, area_type):
    match = re.search(area_type + r'\s*:\s*(\d+\.?\d*)', text)
    if match:
        return float(match.group(1))
    return None
# This function checks if the area is provided in sq.m. and converts it to sqft if needed
def convert_to_sqft(text, area_value):
    if area_value is None:
        return None
    match = re.search(r'{} \((\d+\.?\d*) sq.m.\)'.format(area_value), text)
    if match:
        sq_m_value = float(match.group(1))
        return sq_m_value * 10.7639  # conversion factor from sq.m. to sqft
    return area_value

# Function to extract plot area from 'areaWithType' column
def extract_plot_area(area_with_type):
    match = re.search(r'Plot area (\d+\.?\d*)', area_with_type)
    return float(match.group(1)) if match else None

def convert_scale(row):
    if np.isnan(row['area']) or np.isnan(row['built_up_area']):
        return row['built_up_area']
    else:
        if round(row['area']/row['built_up_area']) == 9.0:
            return row['built_up_area'] * 9
        elif round(row['area']/row['built_up_area']) == 11.0:
            return row['built_up_area'] * 10.7
        else:
            return row['built_up_area']

def load_df(csv_path):
    df = pd.read_csv(csv_path)
    # areawithtype
    df.sample(5)[['price','area','areaWithType']]
    # Extract Super Built up area and convert to sqft if needed
    df['super_built_up_area'] = df['areaWithType'].apply(get_super_built_up_area)
    df['super_built_up_area'] = df.apply(lambda x: convert_to_sqft(x['areaWithType'], x['super_built_up_area']), axis=1)

    # Extract Built Up area and convert to sqft if needed
    df['built_up_area'] = df['areaWithType'].apply(lambda x: get_area(x, 'Built Up area'))
    df['built_up_area'] = df.apply(lambda x: convert_to_sqft(x['areaWithType'], x['built_up_area']), axis=1)

    # Extract Carpet area and convert to sqft if needed
    df['carpet_area'] = df['areaWithType'].apply(lambda x: get_area(x, 'Carpet area'))
    df['carpet_area'] = df.apply(lambda x: convert_to_sqft(x['areaWithType'], x['carpet_area']), axis=1)
    df.duplicated().sum()

    df[~((df['super_built_up_area'].isnull()) | (df['built_up_area'].isnull()) | (df['carpet_area'].isnull()))][['price','property_type','area','areaWithType','super_built_up_area','built_up_area','carpet_area']].shape

    df[df['areaWithType'].str.contains('Plot')][['price','property_type','area','areaWithType','super_built_up_area','built_up_area','carpet_area']].head(5)

    all_nan_df = df[((df['super_built_up_area'].isnull()) & (df['built_up_area'].isnull()) & (df['carpet_area'].isnull()))][['price','property_type','area','areaWithType','super_built_up_area','built_up_area','carpet_area']]

    all_nan_df['built_up_area'] = all_nan_df['areaWithType'].apply(extract_plot_area)

    #Update the original dataframe
    #gurgaon_properties.update(filtered_rows)
    all_nan_df['built_up_area'] = all_nan_df.apply(convert_scale,axis=1)
    return df 


def main():
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    # input file
    csv_path = BASE_DIR /"data"/"raw"/"preprocessing"/"gurgaon_properties_cleaned_v1.csv"
    # output file
    output_dir = BASE_DIR /"data"/"raw"/"features"/"gurgaon_properties_cleaned_v2.csv"
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

