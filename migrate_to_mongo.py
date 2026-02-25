import json
from pymongo import MongoClient

def migrate():
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['housing_db']
        
        # 1. Migrate City Pricing Data
        print("Migrating City Pricing Data...")
        with open('city_pricing_data.json', 'r', encoding='utf-8') as f:
            pricing_data = json.load(f)
        
        # We'll store the entire config but split cities for easier querying if needed
        # Actually, store the whole doc as a 'config' and also create a 'cities' collection
        
        # Store metadata/multipliers in 'metadata' collection
        metadata = {
            "property_type_multipliers": pricing_data['property_type_multipliers'],
            "bhk_multipliers": pricing_data['bhk_multipliers'],
            "locality_adjustments": pricing_data['locality_adjustments'],
            "age_depreciation": pricing_data['age_depreciation'],
            "furnishing_premiums": pricing_data['furnishing_premiums'],
            "amenities_premium": pricing_data['amenities_premium'],
            "rental_config": pricing_data['rental_config']
        }
        db.metadata.delete_many({}) # Clear existing
        db.metadata.insert_one(metadata)
        
        # Store cities in 'cities' collection
        db.cities.delete_many({})
        city_docs = []
        for city_name, city_info in pricing_data['cities'].items():
            doc = city_info.copy()
            doc['name'] = city_name
            city_docs.append(doc)
        
        if city_docs:
            db.cities.insert_many(city_docs)
            print(f"Successfully migrated {len(city_docs)} cities.")

        # 2. Migrate Users (if users.json exists)
        try:
            print("Migrating Users...")
            with open('users.json', 'r', encoding='utf-8') as f:
                users = json.load(f)
            db.users.delete_many({})
            if isinstance(users, list) and len(users) > 0:
                db.users.insert_many(users)
                print(f"Successfully migrated {len(users)} users.")
            else:
                print("users.json is empty or not a list, skipping.")
        except FileNotFoundError:
            print("users.json not found, skipping user migration.")

        # 3. Migrate Prediction History (if predictions_history.json exists)
        try:
            print("Migrating Predictions...")
            with open('predictions_history.json', 'r', encoding='utf-8') as f:
                predictions = json.load(f)
            db.predictions.delete_many({})
            if isinstance(predictions, list) and len(predictions) > 0:
                db.predictions.insert_many(predictions)
                print(f"Successfully migrated {len(predictions)} predictions.")
            else:
                print("predictions_history.json is empty or not a list, skipping.")
        except FileNotFoundError:
            print("predictions_history.json not found, skipping predictions migration.")

        # 4. Migrate Help Tickets (if help_tickets.json exists)
        try:
            print("Migrating Help Tickets...")
            with open('help_tickets.json', 'r', encoding='utf-8') as f:
                tickets = json.load(f)
            db.tickets.delete_many({})
            if isinstance(tickets, list) and len(tickets) > 0:
                db.tickets.insert_many(tickets)
                print(f"Successfully migrated {len(tickets)} tickets.")
            else:
                print("help_tickets.json is empty or not a list, skipping.")
        except FileNotFoundError:
            print("help_tickets.json not found, skipping tickets migration.")

        print("Migration completed successfully!")

    except Exception as e:
        print(f"An error occurred during migration: {e}")

if __name__ == "__main__":
    migrate()
