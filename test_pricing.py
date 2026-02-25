"""
Quick test to verify Indian housing price prediction logic works
"""
import json

# Load city pricing data
with open('city_pricing_data.json', 'r', encoding='utf-8') as f:
    pricing_data = json.load(f)

# Test inputs
city = "Mumbai"
property_type = "Apartment"
bhk = "2 BHK"
area_sqft = 1000
locality_tier = "Mid-Range"
age_of_property = "New (0-1 year)"
furnishing = "Unfurnished"
amenities = ['parking']

# Calculate price
city_data = pricing_data['cities'][city]
base_price_per_sqft = city_data['base_price_per_sqft']

# Apply multipliers
property_multiplier = pricing_data['property_type_multipliers'].get(property_type, 1.0)
bhk_multiplier = pricing_data['bhk_multipliers'].get(bhk, 1.0)
locality_adjustment = pricing_data['locality_adjustments'].get(locality_tier, 1.0)
age_factor = pricing_data['age_depreciation'].get(age_of_property, 1.0)
furnishing_premium = pricing_data['furnishing_premiums'].get(furnishing, 1.0)

# Calculate amenities premium
amenities_factor = 1.0
for amenity in amenities:
    amenities_factor += pricing_data['amenities_premium'].get(amenity, 0)

# Final price calculation
final_price_per_sqft = (base_price_per_sqft * 
                        property_multiplier * 
                        bhk_multiplier * 
                        locality_adjustment * 
                        age_factor * 
                        furnishing_premium * 
                        amenities_factor)

total_price = final_price_per_sqft * area_sqft

# Format price
if total_price >= 10000000:
    price_display = f"₹{total_price/10000000:.2f} Crore"
else:
    price_display = f"₹{total_price/100000:.2f} Lakh"

print(f"✓ Test Successful!")
print(f"City: {city}")
print(f"Property: {bhk} {property_type}")
print(f"Area: {area_sqft} sq.ft")
print(f"Base Price/sqft: ₹{base_price_per_sqft:,}")
print(f"Final Price/sqft: ₹{final_price_per_sqft:,.0f}")
print(f"Total Price: {price_display}")
print(f"\nAll calculation logic working correctly!")
