import pickle
import sys

try:
    with open('Housing_Model', 'rb') as f:
        model = pickle.load(f)
    print(f"Type: {type(model)}")
    if hasattr(model, 'n_features_in_'):
        print(f"Features count: {model.n_features_in_}")
    if hasattr(model, 'feature_names_in_'):
        print(f"Features: {list(model.feature_names_in_)}")
except Exception as e:
    print(f"Error: {e}")
