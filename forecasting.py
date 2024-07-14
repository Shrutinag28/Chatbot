import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler

class SalesForecaster:
    def __init__(self):
        # Load the sales forecasting model
        self.model = self.train_model()
    
    def train_model(self):
        # Load the CSV files
        csv_features_path = 'features.csv'
        csv_stores_path = 'stores.csv'
        csv_train_path = 'train.csv'
        
        stores_df = pd.read_csv(csv_stores_path)
        features_df = pd.read_csv(csv_features_path)
        train_df = pd.read_csv(csv_train_path)
        
        # Preprocess the data
        df = train_df.merge(features_df, on=['Store', 'Date'], how='inner').merge(stores_df, on=['Store'], how='inner')
        df.drop(['IsHoliday_y'], axis=1, inplace=True)
        df.rename(columns={'IsHoliday_x':'IsHoliday'}, inplace=True)
        df = df.loc[df['Weekly_Sales'] > 0]
        
        # Handle special dates
        df.loc[(df['Date'] == '2010-02-12')|(df['Date'] == '2011-02-11')|(df['Date'] == '2012-02-10'),'Super_Bowl'] = True
        df.loc[(df['Date'] != '2010-02-12')&(df['Date'] != '2011-02-11')&(df['Date'] != '2012-02-10'),'Super_Bowl'] = False
        df.loc[(df['Date'] == '2010-09-10')|(df['Date'] == '2011-09-09')|(df['Date'] == '2012-09-07'),'Labor_Day'] = True
        df.loc[(df['Date'] != '2010-09-10')&(df['Date'] != '2011-09-09')&(df['Date'] != '2012-09-07'),'Labor_Day'] = False
        df.loc[(df['Date'] == '2010-11-26')|(df['Date'] == '2011-11-25'),'Thanksgiving'] = True
        df.loc[(df['Date'] != '2010-11-26')&(df['Date'] != '2011-11-25'),'Thanksgiving'] = False
        df.loc[(df['Date'] == '2010-12-31')|(df['Date'] == '2011-12-30'),'Christmas'] = True
        df.loc[(df['Date'] != '2010-12-31')&(df['Date'] != '2011-12-30'),'Christmas'] = False
        
        df = df.fillna(0)
        df["Date"] = pd.to_datetime(df["Date"])
        df['week'] = df['Date'].dt.isocalendar().week
        df['month'] = df['Date'].dt.month
        df['year'] = df['Date'].dt.year
        
        # Encode categorical features
        df_encoded = df.copy()
        type_group = {'A':1, 'B': 2, 'C': 3}
        df_encoded['Type'] = df_encoded['Type'].replace(type_group)
        df_encoded['Super_Bowl'] = df_encoded['Super_Bowl'].astype(bool).astype(int)
        df_encoded['Labor_Day'] = df_encoded['Labor_Day'].astype(bool).astype(int)
        df_encoded['Christmas'] = df_encoded['Christmas'].astype(bool).astype(int)
        df_encoded['IsHoliday'] = df_encoded['IsHoliday'].astype(bool).astype(int)
        
        # Split data into train and test sets
        df_new = df_encoded.copy()
        df_new = df_new.sort_values(by='Date', ascending=True)
        train_data = df_new[:int(0.7*(len(df_new)))]
        test_data = df_new[int(0.7*(len(df_new))):]
        
        target = "Weekly_Sales"
        used_cols = [c for c in df_new.columns.to_list() if c not in [target]]
        
        X_train = train_data[used_cols].drop(['Date'], axis=1)
        X_test = test_data[used_cols].drop(['Date'], axis=1)
        y_train = train_data[target]
        y_test = test_data[target]
        
        # Train the model
        rf = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1, max_depth=35, max_features='sqrt', min_samples_split=10)
        scaler = RobustScaler()
        pipe = make_pipeline(scaler, rf)
        pipe.fit(X_train, y_train)
        
        return pipe
    
    def predict(self, sales_data):
        # Use the trained model to predict future sales
        forecast = self.model.predict(sales_data)
        return forecast