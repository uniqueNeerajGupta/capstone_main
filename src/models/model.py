import numpy as np
import numpy as np
import pandas as pd
from pathlib import Path
import re
import os 
import pickle
import pandas as pd
import category_encoders as ce
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, KFold


def model(csv_path):

    # Load data
    df = pd.read_csv(csv_path)

    # Furnishing mapping
    df['furnishing_type'] = df['furnishing_type'].replace({
        0.0: 'unfurnished',
        1.0: 'semifurnished',
        2.0: 'furnished'
    })

    # Split X, y
    X = df.drop(columns=['price'])
    y = df['price']
    y_transformed = np.log1p(y)

    # Parameters
    param_grid = {
        'regressor__n_estimators': [50, 100, 200, 300],
        'regressor__max_depth': [None, 10, 20, 30],
        'regressor__max_samples': [0.1, 0.25, 0.5, 1.0],
        'regressor__max_features': ['auto', 'sqrt']
    }

    columns_to_encode = [
        'property_type', 'sector', 'balcony',
        'agePossession', 'furnishing_type',
        'luxury_category', 'floor_category'
    ]

    # Preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(),
             ['bedRoom', 'bathroom', 'built_up_area', 'servant room', 'store room']),
            ('cat', OrdinalEncoder(), columns_to_encode),
            ('cat1', OneHotEncoder(drop='first', sparse_output=False), ['agePossession']),
            ('target_enc', ce.TargetEncoder(), ['sector'])
        ],
        remainder='passthrough'
    )

    # Pipeline
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(random_state=42))
    ])

    # CV
    kfold = KFold(n_splits=10, shuffle=True, random_state=42)

    # GridSearch
    search = GridSearchCV(
        pipeline,
        param_grid,
        cv=kfold,
        scoring='r2',
        n_jobs=-1,
        verbose=4
    )

    search.fit(X, y_transformed)


    

    # input file
    # csv_path = BASE_DIR / "data" / "processed" / "gurgaon_properties_outlier_treated.csv"

    # output file
    # output_dir = BASE_DIR / "data" / "raw" / "outlier" 
    # output_dir.mkdir(parents=True, exist_ok=True)


    # output_path = output_dir / "gurgaon_properties_outlier_treaed.csv"

    
    print("best_model", search.best_estimator_)
    print("best_score", search.best_score_)
    print("best_params", search.best_params_)
    return  search.best_estimator_ , X
    


def main():
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    # input file
    
    csv_path = BASE_DIR / "data" / "interim" / "gurgaon_properties_post_feature_selection_v2.csv"
    pipeline , X = model(csv_path)

    output_dir = BASE_DIR / "data" / "raw" / "model_df" 
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "pipeline.pkl"

    with open(output_path, 'wb') as file:
        pickle.dump(pipeline, file)

    output_dir1 = BASE_DIR / "data" / "raw" / "model_pipeline" 
    output_dir1.mkdir(parents=True, exist_ok=True)
    output_path1 = output_dir1 / "df.pkl"

    with open(output_path1, 'wb') as file:
        pickle.dump(X, file)

    # 

    print("working")
    # print(df['price'])

if __name__ == "__main__":
    main()