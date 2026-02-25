import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pickle

# Load data
print("Loading data...")
data = pd.read_csv("Data_For_Model.csv", index_col=0)

# Drop unnecessary columns as per notebook
columns_to_drop = ["Lng", "Lat", "ladderRatio", "fiveYearsProperty", "subway", "floor_height",
                   "buildingType_2.0", "buildingType_3.0", "buildingType_4.0", "district_2",
                   "district_3", "district_4", "district_5", "district_6", "district_7",
                   "district_8", "district_9", "district_10", "district_11", "district_12",
                   "district_13", "floor_type_低", "floor_type_底", "floor_type_未知",
                   "floor_type_顶", "floor_type_高"]

# Check if columns exist before dropping to avoid errors if data is different
existing_columns_to_drop = [col for col in columns_to_drop if col in data.columns]
data.drop(columns=existing_columns_to_drop, inplace=True, axis=1)

# Prepare features and target
X = data.drop(['totalPrice'], axis=1)
y = data['totalPrice']

# Train model
print("Training model...")
rfm = RandomForestRegressor(max_depth=None, min_samples_leaf=5, min_samples_split=6,
                            n_estimators=120, verbose=2, n_jobs=-1)
rfm.fit(X, y)

# Save model
print("Saving model to Housing_Model...")
pickle.dump(rfm, open('Housing_Model', 'wb'))
print("Model saved successfully.")
