import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
import seaborn as sns 
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
import re
import os 
def categorize_luxury(score):
    if 0 <= score < 50:
        return "Low"
    elif 50 <= score < 150:
        return "Medium"
    elif 150 <= score <= 175:
        return "High"
    else:
        return None  # or "Undefined" or any other label for scores outside the defined bins
    
def categorize_floor(floor):
    if 0 <= floor <= 2:
        return "Low Floor"
    elif 3 <= floor <= 10:
        return "Mid Floor"
    elif 11 <= floor <= 51:
        return "High Floor"
    else:
        return None  # or "Undefined" or any other label for floors outside the defined bins
    

def outlier(csv_path):
    df = pd.read_csv(csv_path)
    train_df = df.drop(columns=['society','price_per_sqft'])
    train_df['luxury_category'] = train_df['luxury_score'].apply(categorize_luxury)
    train_df['floor_category'] = train_df['floorNum'].apply(categorize_floor)
    train_df.drop(columns=['floorNum','luxury_score'],inplace=True)
    data_label_encoded = train_df.copy()
    categorical_cols = train_df.select_dtypes(include=['object']).columns

    # encoding
    for col in categorical_cols:
         oe = OrdinalEncoder()
         data_label_encoded[col] = oe.fit_transform(data_label_encoded[[col]])
         # print(oe.categories_)
    X_label = data_label_encoded.drop('price', axis=1)
    y_label = data_label_encoded['price']
    # print(X_label,y_label)

    ### Technique 1 - Correlation Analysis
    sns.heatmap(data_label_encoded.corr())
    fi_df1 = data_label_encoded.corr()['price'].iloc[1:].to_frame().reset_index().rename(columns={'index':'feature','price':'corr_coeff'})
    fi_df1


    # random forest 
    from sklearn.ensemble import RandomForestRegressor

    # Train a Random Forest regressor on label encoded data
    rf_label = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_label.fit(X_label, y_label)

    # Extract feature importance scores for label encoded data
    fi_df2 = pd.DataFrame({
    'feature': X_label.columns,
    'rf_importance': rf_label.feature_importances_
    }).sort_values(by='rf_importance', ascending=False)

    # fi_df2
    # gradient
    from sklearn.ensemble import GradientBoostingRegressor

    # Train a Random Forest regressor on label encoded data
    gb_label = GradientBoostingRegressor()
    gb_label.fit(X_label, y_label)

    # Extract feature importance scores for label encoded data
    fi_df3 = pd.DataFrame({
    'feature': X_label.columns,
    'gb_importance': gb_label.feature_importances_
    }).sort_values(by='gb_importance', ascending=False)

    # fi_df3
    ### Technique 4 - Permutation Importance
    
    X_train_label, X_test_label, y_train_label, y_test_label = train_test_split(X_label, y_label, test_size=0.2, random_state=42)

    # Train a Random Forest regressor on label encoded data
    rf_label = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_label.fit(X_train_label, y_train_label)

    # Calculate Permutation Importance
    perm_importance = permutation_importance(rf_label, X_test_label, y_test_label, n_repeats=30, random_state=42)

    # Organize results into a DataFrame
    fi_df4 = pd.DataFrame({
    'feature': X_label.columns,
    'permutation_importance': perm_importance.importances_mean
    }).sort_values(by='permutation_importance', ascending=False)

    # fi_df4

    ### Technique 5 - LASSO
    from sklearn.linear_model import Lasso
    from sklearn.preprocessing import StandardScaler

    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_label)

    # Train a LASSO regression model
    # We'll use a relatively small value for alpha (the regularization strength) for demonstration purposes
    lasso = Lasso(alpha=0.01, random_state=42)
    lasso.fit(X_scaled, y_label)

    # Extract coefficients
    fi_df5 = pd.DataFrame({
    'feature': X_label.columns,
    'lasso_coeff': lasso.coef_
    }).sort_values(by='lasso_coeff', ascending=False)

    # fi_df5

    ### Technique 6 - RFE
    from sklearn.feature_selection import RFE
    estimator = RandomForestRegressor()
    # Apply RFE on the label-encoded and standardized training data
    selector_label = RFE(estimator, n_features_to_select=X_label.shape[1], step=1)
    selector_label = selector_label.fit(X_label, y_label)
    selected_features = X_label.columns[selector_label.support_]
    selected_coefficients = selector_label.estimator_.feature_importances_

    # Organize the results into a DataFrame
    fi_df6 = pd.DataFrame({
    'feature': selected_features,
    'rfe_score': selected_coefficients
    }).sort_values(by='rfe_score', ascending=False)

    # fi_df6
    import shap

    # Compute SHAP values using the trained Random Forest model
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_label, y_label)

    explainer = shap.TreeExplainer(rf)
    shap_values = explainer.shap_values(X_label)
 
    # Summing the absolute SHAP values across all samples to get an overall measure of feature importance
    shap_sum = np.abs(shap_values).mean(axis=0)

    # shap_values
    fi_df8 = pd.DataFrame({
    'feature': X_label.columns,
    'SHAP_score': np.abs(shap_values).mean(axis=0)
    }).sort_values(by='SHAP_score', ascending=False)

    # fi_df8
    final_fi_df = fi_df1.merge(fi_df2,on='feature').merge(fi_df3,on='feature').merge(fi_df4,on='feature').merge(fi_df5,on='feature').merge(fi_df6,on='feature').merge(fi_df8,on='feature').set_index('feature')
    # normalize the score
    final_fi_df = final_fi_df.divide(final_fi_df.sum(axis=0), axis=1)
    print(final_fi_df)


    
    #  prove
    # with all the cols 
    from sklearn.model_selection import cross_val_score

    rf = RandomForestRegressor(n_estimators=100, random_state=42)

    scores = cross_val_score(rf, X_label, y_label, cv=5, scoring='r2')
    rf = RandomForestRegressor(n_estimators=100, random_state=42)

    scores = cross_val_score(rf, X_label.drop(columns=['pooja room', 'study room', 'others']), y_label, cv=5, scoring='r2')
    scores.mean()
    export_df = X_label.drop(columns=['pooja room', 'study room', 'others'])
    # export_df['price'] = y_label
    
    return df
















def main():
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    # input file
    csv_path = BASE_DIR / "data" / "raw" / "imputation" / "gurgaon_properties_missing_value_imputation.csv"

    # output file
    output_dir = BASE_DIR / "data" / "raw" / "features_one" 
    output_dir.mkdir(parents=True, exist_ok=True)


    output_path = output_dir / "gurgaon_properties_post_features_selection.csv"

    # load & process
    df = outlier(csv_path)

    # save 
    df.to_csv(output_path, index=False)
    # print(f"✅ Data saved to: {output_path}")

    print("working")
    # print(X_label)
    # print(df['price'])




if __name__ == "__main__":
    main()
