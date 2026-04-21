# @Author ---> Tufail Ahmad Mir

from flask import Flask,request,render_template,redirect,url_for,session,jsonify,flash

from datetime import datetime
import os
import json
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()


app=Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')

# --- ML Scaling Configuration (MinMaxScaler Parameters) ---
# Derived from After_EDA dataset for "Production Parity"
SCALERS = {
    'followers': {'min': 0, 'max': 1143},
    'square': {'min': 7.3, 'max': 460.1},
    'livingRoom': {'min': 0, 'max': 8},
    'drawingRoom': {'min': 0, 'max': 5},
    'kitchen': {'min': 0, 'max': 3},
    'bathRoom': {'min': 0, 'max': 7},
    'Lng': {'min': 116.07, 'max': 116.71},
    'Lat': {'min': 39.63, 'max': 40.25},
    'communityAverage': {'min': 1000, 'max': 150000}, # Estimated from EDA
    'ladderRatio': {'min': 0, 'max': 1},
    'fiveYearsProperty': {'min': 0, 'max': 1},
    'subway': {'min': 0, 'max': 1},
    'floor_height': {'min': 1, 'max': 50}
}

def normalize_value(val, feature):
    if feature not in SCALERS:
        return val
    s = SCALERS[feature]
    return (val - s['min']) / (s['max'] - s['min'])


# Admin Credentials
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@housing.com')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')


# --- MongoDB Configuration ---
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client['housing_db']

# Mapping for property images with expanded city support
PROPERTY_IMAGES = {
    "types": {
        "Apartment": "apartment_general.png",
        "Independent House": "house_general.png",
        "Villa": "villa_general.png",
        "Builder Floor": "apartment_general.png" # Fixed broken reference
    },
    "cities": {
        "Mumbai": {
            "Apartment": "mumbai_apartment.png",
            "Independent House": "mumbai_apartment.png",
            "Villa": "mumbai_apartment.png",
            "Builder Floor": "mumbai_apartment.png"
        },
        "Bangalore": {
            "Villa": "bangalore_villa.png",
            "Apartment": "apartment_general.png",
            "Independent House": "house_general.png",
            "Builder Floor": "house_general.png"
        },
        "Delhi NCR": {
            "Independent House": "delhi_house.png",
            "Apartment": "delhi_house.png",
            "Villa": "delhi_house.png",
            "Builder Floor": "delhi_house.png"
        },
        "Gurugram": {
            "Builder Floor": "apartment_general.png",
            "Apartment": "apartment_general.png",
            "Villa": "villa_general.png",
            "Independent House": "house_general.png"
        },
        "Hyderabad": {
            "Apartment": "apartment_general.png",
            "Villa": "villa_general.png",
            "Independent House": "house_general.png",
            "Builder Floor": "apartment_general.png"
        },
        "Pune": {
            "Apartment": "apartment_general.png",
            "Independent House": "house_general.png",
            "Villa": "villa_general.png",
            "Builder Floor": "apartment_general.png"
        },
        "Chennai": {
            "Apartment": "apartment_general.png",
            "Independent House": "house_general.png",
            "Villa": "villa_general.png",
            "Builder Floor": "apartment_general.png"
        }
    }
}

# Regional mapping for intelligent image selection
CITY_REGIONS = {
    "North": ["Delhi NCR", "Gurugram", "Noida", "Chandigarh", "Lucknow", "Jaipur", "Ludhiana", "Jammu", "Srinagar", "New Delhi", "Dwarka", "Rohini", "Janakpuri", "Pitampura", "Panipat", "Ambala", "Karnal", "Dharamshala", "Solan", "Mandi", "Kullu", "Anantnag", "Baramulla", "Kathua", "Ajmer", "Haridwar", "Roorkee", "Haldwani", "Rudrapur"],
    "South": ["Bangalore", "Hyderabad", "Chennai", "Kochi", "Visakhapatnam", "Vijayawada", "Coimbatore", "Belgaum", "Nizamabad", "Karimnagar", "Khammam", "Salem", "Guntur", "Nellore", "Kurnool", "Thrissur", "Kollam"],
    "West": ["Mumbai", "Pune", "Ahmedabad", "Surat", "Vadodara", "Nashik", "Nagpur", "Margao", "Vasco da Gama", "Mapusa", "Ponda", "Indore", "Bhopal", "Jabalpur", "Gwalior", "Ujjain"],
    "East": ["Kolkata", "Patna", "Guwahati", "Bhubaneswar", "Ranchi", "Asansol", "Howrah", "Dibrugarh", "Silchar", "Jorhat", "Nagaon", "Gaya", "Bhagalpur", "Muzaffarpur", "Purnia", "Bhilai", "Bilaspur", "Korba", "Rajnandgaon", "Dhanbad", "Bokaro", "Deoghar", "Rourkela", "Berhampur", "Sambalpur", "Siliguri", "Durgapur"]
}

def get_property_image(city, property_type):
    """Dynamically select property image based on city and type"""
    # 1. Exact City Match
    if city in PROPERTY_IMAGES['cities'] and property_type in PROPERTY_IMAGES['cities'][city]:
        return PROPERTY_IMAGES['cities'][city][property_type]
    
    # 2. Regional Match logic
    for region, cities in CITY_REGIONS.items():
        if city in cities:
            if region == "North":
                if property_type == "Independent House": return "delhi_house.png"
                return "apartment_general.png"
            elif region == "South":
                if property_type == "Villa": return "bangalore_villa.png"
                return "apartment_general.png"
            elif region == "West":
                if property_type in ["Apartment", "Builder Floor"]: return "mumbai_apartment.png"
                return "house_general.png"
    
    # 3. Default fallback by type
    return PROPERTY_IMAGES['types'].get(property_type, "apartment_general.png")

def load_users():
    users = list(db.users.find({}, {'_id': 0}))
    return {'users': users}

def save_users(data):
    # This function was used for the whole list, in Mongo we'd usually insert one
    # but for compatibility with existing code where it might be used:
    db.users.delete_many({})
    if data['users']:
        db.users.insert_many(data['users'])

def load_predictions():
    predictions = list(db.predictions.find({}, {'_id': 0}).sort('timestamp', -1))
    return {'predictions': predictions}

def save_prediction(prediction_data):
    db.predictions.insert_one(prediction_data)

def save_ticket(ticket_data):
    db.tickets.insert_one(ticket_data)

def get_metadata():
    return db.metadata.find_one({}, {'_id': 0})

def calculate_emi(principal, annual_rate, tenure_years):
    """Calculate EMI for home loan"""
    monthly_rate = annual_rate / (12 * 100)
    tenure_months = tenure_years * 12
    if monthly_rate == 0:
        return principal / tenure_months
    emi = principal * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (((1 + monthly_rate) ** tenure_months) - 1)
    emi = principal * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (((1 + monthly_rate) ** tenure_months) - 1)
    return round(emi, 2)

def get_investment_score(city_tier, locality_tier, age_of_property, amenities_count):
    """Calculate an investment score from 1-10"""
    score = 5.0 # Base score
    
    # Tier logic
    if city_tier == 1: score += 1.5 # Stable growth
    else: score += 2.0 # Higher growth ceiling
    
    # Locality logic
    if locality_tier == "Premium": score += 2.0
    elif locality_tier == "Mid-Range": score += 1.0
    else: score -= 0.5
    
    # Age logic
    if age_of_property == "New (0-1 year)": score += 1.5
    elif age_of_property == "10+ years": score -= 1.0
    
    # Amenities
    score += (amenities_count * 0.3)
    
    return min(max(round(score, 1), 1.0), 10.0)

def get_neighborhood_ratings(locality_tier):
    """Return ratings for various lifestyle factors"""
    if locality_tier == "Premium":
        return {"Safety": 9, "Connectivity": 8, "Lifestyle": 10, "Greenery": 9}
    elif locality_tier == "Mid-Range":
        return {"Safety": 7, "Connectivity": 9, "Lifestyle": 7, "Greenery": 6}
    else:
        return {"Safety": 6, "Connectivity": 6, "Lifestyle": 4, "Greenery": 5}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Admin Login Check
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['user'] = {'name': 'Admin', 'email': email, 'is_admin': True}
            return redirect(url_for('admin'))

        # User Login Check
        users_data = load_users()
        for user in users_data['users']:
            if user['email'] == email and user['password'] == password:
                session['user'] = {'name': user['name'], 'email': email, 'is_admin': False}
                return redirect(url_for('home'))
        
        return render_template('login.html', error="Invalid email or password")

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not name or not email or not password:
            return render_template('signup.html', error="All fields are required")

        # Check if user already exists in MongoDB
        existing_user = db.users.find_one({'email': email})
        if existing_user:
            return render_template('signup.html', error="Email already registered")

        # Create new user
        new_user = {
            'name': name,
            'email': email,
            'password': password, # In production, hash this!
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        db.users.insert_one(new_user)
        
        session['user'] = {'name': name, 'email': email, 'is_admin': False}
        return redirect(url_for('home'))

    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


@app.route('/about')
def about():
    user = session.get('user')
    return render_template('about.html', user=user)


@app.route('/contact')
def contact():
    user = session.get('user')
    return render_template('contact.html', user=user)


@app.route('/admin')
def admin():
    user = session.get('user')
    if not user or not user.get('is_admin'):
        return redirect(url_for('login'))
    # Calculate Stats
    # Calculate Stats from MongoDB
    total_users = db.users.count_documents({})
    
    tickets = list(db.tickets.find({}))
    total_tickets = len(tickets)
    pending_tickets = sum(1 for t in tickets if t.get('status') == 'pending')
    resolved_tickets = sum(1 for t in tickets if t.get('status') == 'resolved')
            
    stats = {
        'total_users': total_users,
        'total_tickets': total_tickets,
        'pending_tickets': pending_tickets,
        'resolved_tickets': resolved_tickets
    }

    return render_template('admin.html', user=user, stats=stats)


@app.route('/submit_ticket', methods=['POST'])
def submit_ticket():
    try:
        # Get ticket data from request
        ticket_data = request.json
        
        # Ticket ID will be generated by the client or here if missing
        if not ticket_data.get('id'):
            ticket_data['id'] = f"TICK-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
        ticket_data['status'] = 'pending'
        ticket_data['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        db.tickets.insert_one(ticket_data)
        
        return jsonify({'success': True, 'message': 'Help request submitted successfully! Our team will respond via email soon.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})


@app.route('/get_tickets', methods=['GET'])
def get_tickets():
    # Protect this route too
    user = session.get('user')
    if not user or not user.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        tickets = list(db.tickets.find({}, {'_id': 0}))
        return jsonify({'tickets': tickets})
    except Exception as e:
        return jsonify({'tickets': [], 'error': str(e)})


@app.route('/update_ticket_status', methods=['POST'])
def update_ticket_status():
    # Protect this route too
    user = session.get('user')
    if not user or not user.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    try:
        ticket_data = request.json
        ticket_id = ticket_data.get('ticket_id')
        new_status = ticket_data.get('status', 'resolved')
        
        result = db.tickets.update_one(
            {'id': ticket_id},
            {'$set': {
                'status': new_status,
                'resolved_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S') if new_status == 'resolved' else None
            }}
        )
        
        if result.modified_count > 0:
            return jsonify({'success': True, 'message': 'Ticket status updated successfully'})
        else:
            return jsonify({'success': False, 'message': 'Ticket not found or status already set'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})
@app.route('/reply_ticket', methods=['POST'])
def reply_ticket():
    user = session.get('user')
    if not user or not user.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    try:
        data = request.json
        ticket_id = data.get('ticket_id')
        reply_message = data.get('reply_message')
        
        if not ticket_id or not reply_message:
             return jsonify({'success': False, 'message': 'Missing ticket ID or reply message'}), 400

        result = db.tickets.update_one(
            {'id': ticket_id},
            {'$set': {
                'reply': reply_message,
                'replied_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'resolved',
                'resolved_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }}
        )
        
        if result.modified_count > 0:
            return jsonify({'success': True, 'message': 'Reply sent and ticket resolved successfully'})
        else:
            return jsonify({'success': False, 'message': 'Ticket not found'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})


@app.route('/')
def home():
    user = session.get('user')
    # Load and organize cities by state from MongoDB
    cities = list(db.cities.find({}, {'name': 1, 'state': 1, '_id': 0}))
    
    cities_by_state = {}
    for city_doc in cities:
        city = city_doc['name']
        state = city_doc['state']
        if state not in cities_by_state:
            cities_by_state[state] = []
        cities_by_state[state].append(city)
    
    # Sort states and cities
    sorted_states = sorted(cities_by_state.keys())
    for state in sorted_states:
        cities_by_state[state].sort()
        
    return render_template('index.html', user=user, cities_by_state=cities_by_state, states=sorted_states)




         
@app.route('/api/city_areas/<city_name>')
def get_city_areas_api(city_name):
    """API endpoint to get sub-areas for a specific city"""
    try:
        city_data = db.cities.find_one({'name': city_name}, {'areas': 1, '_id': 0})
        if city_data and 'areas' in city_data:
            return jsonify({'success': True, 'areas': city_data['areas']})
        return jsonify({'success': False, 'message': 'No areas found for this city'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

def get_price_prediction(city, property_type, bhk, area_sqft, locality_tier, age_of_property, furnishing, amenities, area_multiplier=1.0):
    # Load metadata and city data from MongoDB
    pricing_data = get_metadata()
    city_data = db.cities.find_one({'name': city}, {'_id': 0})
    
    if not city_data:
        return None, "Invalid City"

    # Calculate price
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
    
    # Final price calculation with AREA MULTIPLIER
    final_price_per_sqft = (base_price_per_sqft * 
                            property_multiplier * 
                            bhk_multiplier * 
                            locality_adjustment * 
                            age_factor * 
                            furnishing_premium * 
                            amenities_factor *
                            area_multiplier)
    
    total_price = final_price_per_sqft * area_sqft
    return total_price, final_price_per_sqft

def get_rent_prediction(city, property_type, area_sqft, locality_tier, furnishing, duration='Monthly', area_multiplier=1.0):
    """Estimate rent based on property value, config and duration"""
    # First get the estimated property price
    price, _ = get_price_prediction(city, property_type, "2 BHK", area_sqft, locality_tier, "New (0-1 year)", furnishing, [], area_multiplier=area_multiplier)
    
    if price is None:
        return None
        
    # Load rental config from MongoDB
    pricing_data = get_metadata()
    rent_config = pricing_data.get('rental_config', {})
    base_yield = rent_config.get('base_annual_yield', 0.03)
    
    # Apply multipliers
    type_mult = rent_config.get('type_multipliers', {}).get(property_type, 1.0)
    loc_mult = rent_config.get('locality_multipliers', {}).get(locality_tier, 1.0)
    fur_mult = rent_config.get('furnishing_multipliers', {}).get(furnishing, 1.0)
    
    # Calculate base annual rent
    annual_rent = price * base_yield * type_mult * loc_mult * fur_mult
    
    # Monthly rent is the baseline
    monthly_rent = annual_rent / 12
    
    if duration == 'Daily':
        # Daily is usually ~15-20% higher than monthly pro-rata
        return round((monthly_rent / 30) * 1.5, -1) # Round to nearest 10
    elif duration == 'Weekly':
        # Weekly is ~10% higher than monthly pro-rata
        return round((monthly_rent / 4) * 1.2, -1)
    else: # Monthly
        return round(monthly_rent, -2) # Round to nearest 100

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    user = session.get('user')
    
    # Load and organize cities by state from MongoDB
    cities = list(db.cities.find({}, {'name': 1, 'state': 1, '_id': 0}))
    
    cities_by_state = {}
    for city_doc in cities:
        city = city_doc['name']
        state = city_doc['state']
        if state not in cities_by_state:
            cities_by_state[state] = []
        cities_by_state[state].append(city)
    
    sorted_states = sorted(cities_by_state.keys())
    for state in sorted_states:
        cities_by_state[state].sort()
    
    if request.method == 'POST':
        try:
            # Property 1 Data
            p1_city = request.form.get('p1_city')
            p1_type = request.form.get('p1_type')
            p1_bhk = request.form.get('p1_bhk')
            p1_area = float(request.form.get('p1_area'))
            p1_locality = request.form.get('p1_locality')
            p1_amenities = request.form.getlist('p1_amenities') # Checkbox handling might need adjustment if using same form names
            
            # Simple list for amenities since form handling for lists can be tricky
            # Let's assume basic fields for comparison to keep UI clean
            
            price1, rate1 = get_price_prediction(p1_city, p1_type, p1_bhk, p1_area, p1_locality, "New (0-1 year)", "Unfurnished", [])
            
            # Property 2 Data
            p2_city = request.form.get('p2_city')
            p2_type = request.form.get('p2_type')
            p2_bhk = request.form.get('p2_bhk')
            p2_area = float(request.form.get('p2_area'))
            p2_locality = request.form.get('p2_locality')
            
            price2, rate2 = get_price_prediction(p2_city, p2_type, p2_bhk, p2_area, p2_locality, "New (0-1 year)", "Unfurnished", [])
            
            # Calculate EMIs
            emi1 = calculate_emi(price1 * 0.8, 8.5, 20)
            emi2 = calculate_emi(price2 * 0.8, 8.5, 20)
            
            comparison_data = {
                'p1': {
                    'city': p1_city, 'type': p1_type, 'bhk': p1_bhk, 'area': p1_area,
                    'price': price1, 'rate': rate1, 'emi': emi1
                },
                'p2': {
                    'city': p2_city, 'type': p2_type, 'bhk': p2_bhk, 'area': p2_area,
                    'price': price2, 'rate': rate2, 'emi': emi2
                },
                'diff': abs(price1 - price2),
                'cheaper': 'Property 1' if price1 < price2 else 'Property 2'
            }
            
            return render_template('compare.html', user=user, cities_by_state=cities_by_state, states=sorted_states, result=comparison_data)
            
        except Exception as e:
            print(f"Comparison Error: {e}")
            return render_template('compare.html', user=user, cities=cities, error="Error calculating comparison")

    return render_template('compare.html', user=user, cities_by_state=cities_by_state, states=sorted_states)

@app.route('/',methods=['POST'])
def predict():
    user = session.get('user')
    try:
         # Load city data from MongoDB
         city_data = db.cities.find_one({'name': request.form.get('city', '')}, {'_id': 0})
         
         # Get form inputs
         city = request.form.get('city', '')
         property_type = request.form.get('property_type', 'Apartment')
         bhk = request.form.get('bhk', '2 BHK')
         area_sqft = float(request.form.get('area_sqft', 0))
         locality_tier = request.form.get('locality_tier', 'Mid-Range')
         age_of_property = request.form.get('age_of_property', 'New (0-1 year)')
         furnishing = request.form.get('furnishing', 'Unfurnished')
         
         # Dynamic Area Selection
         locality_area = request.form.get('locality_area', 'Main City / Residential')
         area_multiplier = float(request.form.get('area_multiplier', 1.0))

         # Get amenities (checkboxes)
         amenities = []
         if request.form.get('parking'): amenities.append('parking')
         if request.form.get('gym'): amenities.append('gym')
         if request.form.get('pool'): amenities.append('pool')
         if request.form.get('security'): amenities.append('security')
         if request.form.get('lift'): amenities.append('lift')
         if request.form.get('power_backup'): amenities.append('power_backup')
         
         # Validation
         if not city_data:
             return render_template('index.html', error="Please select a valid city!", user=user)
         
         city = city_data['name']
         
         if area_sqft <= 0:
             return render_template('index.html', error="Please enter a valid area in square feet!", user=user)
         
         # Use Helper Function (will query DB inside)
         total_price, final_price_per_sqft = get_price_prediction(city, property_type, bhk, area_sqft, locality_tier, age_of_property, furnishing, amenities, area_multiplier=area_multiplier)
         
         # Format price in Lakhs/Crores
         if total_price >= 10000000:
             price_text = f"₹{total_price/10000000:.2f} Crore"
         else:
             price_text = f"₹{total_price/100000:.2f} Lakh"
         
         # Get property image dynamically
         image_filename = get_property_image(city, property_type)
         
         price_display = {
             'total': price_text,
             'per_sqft': f"₹{final_price_per_sqft:,.0f}/sq.ft",
             'image': image_filename,
             'locality_area': locality_area # Add area to display
         }
         
         price_per_sqft_display = f"₹{final_price_per_sqft:,.0f}"
         
         print(f"Prediction successful for {city}: {price_text}")

         # Fetch city areas for the result page dropdown
         city_areas = city_data.get('areas', [])

         # Prepare inputs for display
         inputs = {
             'city': city,
             'state': city_data['state'],
             'property_type': property_type,
             'bhk': bhk,
             'area_sqft': int(area_sqft),
             'locality_tier': locality_tier,
             'age_of_property': age_of_property,
             'furnishing': furnishing,
             'amenities': ', '.join(amenities) if amenities else 'None',
             'price_per_sqft': price_per_sqft_display,
             'locality_area': locality_area,
             'area_multiplier': area_multiplier,
             'city_areas': city_areas,
         }

         # Calculate Analytics (get tier from city_data we already loaded)
         city_tier = city_data.get('tier', 2)
         investment_score = get_investment_score(city_tier, locality_tier, age_of_property, len(amenities))
         neighborhood_ratings = get_neighborhood_ratings(locality_tier)
         
         # Update results dictionary
         price_display['investment_score'] = investment_score
         price_display['neighborhood_ratings'] = neighborhood_ratings
         price_display['market_sentiment'] = "🔥 High Demand" if city_tier == 1 else "📈 Growing Value"

         # Calculate EMI (assuming 20% down payment, 8.5% interest, 20 years)
         loan_amount = total_price * 0.8  # 80% loan
         emi_monthly = calculate_emi(loan_amount, 8.5, 20)
         total_payment = emi_monthly * 12 * 20
         total_interest = total_payment - loan_amount
         
         emi_data = {
             'loan_amount': loan_amount,
             'down_payment': total_price * 0.2,
             'emi_monthly': emi_monthly,
             'tenure_years': 20,
             'interest_rate': 8.5,
             'total_payment': total_payment,
             'total_interest': total_interest
         }

         # Save prediction history for logged-in users
         if user:
             prediction_record = {
                 'user_email': user.get('email'),
                 'user_name': user.get('name'),
                 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                 'city': city,
                 'property_type': property_type,
                 'bhk': bhk,
                 'area_sqft': int(area_sqft),
                 'predicted_price': total_price,
                 'price_display': price_display
             }
             save_prediction(prediction_record)

         # Load cities for results page dropdown from MongoDB
         _cities = list(db.cities.find({}, {'name': 1, 'state': 1, '_id': 0}))
         _cbs = {}
         for _cd in _cities:
             _cbs.setdefault(_cd['state'], []).append(_cd['name'])
         _ss = sorted(_cbs.keys())
         for _s in _ss:
             _cbs[_s].sort()

         return render_template('index.html',
                              results=price_display,
                              inputs=inputs,
                              emi_data=emi_data,
                              user=user,
                              cities_by_state=_cbs,
                              states=_ss)


    except ValueError as e:
        print(f"ValueError occurred: {e}")
        return render_template('index.html', 
                             error=f"Invalid input: {str(e)}",
                             user=user)
    except Exception as e:
        print(f"Error occurred: {e}")
        return render_template('index.html', 
                             error=f"An error occurred: {str(e)}",
                             user=user)
   

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user or user.get('is_admin'):
        return redirect(url_for('home'))
    
    # Get user's prediction history
    predictions = load_predictions()
    user_predictions = [p for p in predictions['predictions'] if p.get('user_email') == user.get('email')]
    
    # Sort by timestamp descending (newest first)
    user_predictions.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    return render_template('dashboard.html', user=user, predictions=user_predictions[:10])  # Show last 10


@app.route('/rent', methods=['GET', 'POST'])
def rent():
    user = session.get('user')
    
    # Load and organize cities by state from MongoDB
    cities_list = list(db.cities.find({}, {'name': 1, 'state': 1, '_id': 0}))
    
    cities_by_state = {}
    for city_doc in cities_list:
        city = city_doc['name']
        state = city_doc['state']
        if state not in cities_by_state:
            cities_by_state[state] = []
        cities_by_state[state].append(city)
    
    sorted_states = sorted(cities_by_state.keys())
    for state in sorted_states:
        cities_by_state[state].sort()
    
    if request.method == 'POST':
        try:
            city = request.form.get('city')
            p_type = request.form.get('property_type')
            area = float(request.form.get('area_sqft'))
            locality = request.form.get('locality_tier')
            furnishing = request.form.get('furnishing')
            duration = request.form.get('duration', 'Monthly')
            
            est_rent = get_rent_prediction(city, p_type, area, locality, furnishing, duration)
            
            if est_rent:
                # Format rent
                rent_display = f"₹{est_rent:,.0f}/{'day' if duration == 'Daily' else 'week' if duration == 'Weekly' else 'month'}"
                    
                result = {
                    'city': city,
                    'type': p_type,
                    'area': area,
                    'locality': locality,
                    'furnishing': furnishing,
                    'duration': duration,
                    'rent': rent_display
                }
                return render_template('rent.html', user=user, cities_by_state=cities_by_state, states=sorted_states, result=result)
            else:
                return render_template('rent.html', user=user, cities=cities, error="Could not estimate rent.")
                
        except Exception as e:
            print(f"Rent Prediction Error: {e}")
            return render_template('rent.html', user=user, cities=cities, error="Invalid input data.")

    return render_template('rent.html', user=user, cities_by_state=cities_by_state, states=sorted_states)


@app.route('/insights')
def insights():
    user = session.get('user')
    # Load and organize cities by state from MongoDB
    cities_list = list(db.cities.find({}, {'name': 1, 'state': 1, '_id': 0}))
    
    cities_by_state = {}
    for city_doc in cities_list:
        city = city_doc['name']
        state = city_doc['state']
        if state not in cities_by_state:
            cities_by_state[state] = []
        cities_by_state[state].append(city)
    
    sorted_states = sorted(cities_by_state.keys())
    for state in sorted_states:
        cities_by_state[state].sort()
        
    return render_template('insights.html', user=user, cities_by_state=cities_by_state, states=sorted_states)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get('message', '').lower()
        
        # Simple rule-based logic for AI Chatbot
        response = "Hello! I am your AI Housing Assistant. How can I help you today?"
        
        if 'mumbai' in user_msg:
            response = "Mumbai is a Tier 1 city with the highest property rates in India (avg ₹18,000/sq.ft). Investing in suburbs like Thane or Navi Mumbai is currently very popular."
        elif 'delhi' in user_msg:
            response = "Delhi NCR offers varied options. South Delhi is premium, while Noida and Gurgaon are hubs for modern high-rise apartments with great rental yields."
        elif 'bangalore' in user_msg:
            response = "Bangalore, the Silicon Valley of India, has steady growth. Areas near IT parks like Whitefield and Electronic City always have high demand."
        elif 'loan' in user_msg or 'emi' in user_msg:
            response = "I can help with EMI calculations! You can use our built-in calculator on the home page or compare properties to see which one fits your budget."
        elif 'rent' in user_msg:
            response = "You can use our 'Rent' section to estimate rental values for any property across 60+ Indian cities!"
            
        return jsonify({'reply': response})
    except Exception as e:
        return jsonify({'reply': "Sorry, I'm having trouble processing that right now."}), 500

@app.route('/api/market_data')
def market_data():
    # Serve data for Chart.js from MongoDB
    top_cities = ["Mumbai", "Delhi NCR", "Bangalore", "Hyderabad", "Chennai", "Pune", "Kolkata", "Ahmedabad"]
    cities_info = list(db.cities.find({'name': {'$in': top_cities}}, {'name': 1, 'base_price_per_sqft': 1, '_id': 0}))
    
    # Sort according to top_cities list
    cities_map = {c['name']: c['base_price_per_sqft'] for c in cities_info}
    prices = [cities_map.get(city, 0) for city in top_cities]
    
    data = {
        "labels": top_cities,
        "prices": prices
    }
    return jsonify(data)

@app.route('/api/city_insights/<city>')
def city_insights(city):
    try:
        pricing_data = get_metadata()
        city_data = db.cities.find_one({'name': city}, {'_id': 0})
        
        if not city_data:
            return jsonify({'error': 'City not found'}), 404
        
        # Prepare detailed city metrics
        insights = {
            'city': city,
            'base_price': city_data['base_price_per_sqft'],
            'price_range': city_data['price_range'],
            'tier': city_data['tier'],
            'state': city_data['state'],
            'property_types': pricing_data['property_type_multipliers'],
            'localities': {
                'Premium': pricing_data['locality_adjustments']['Premium'] * city_data['base_price_per_sqft'],
                'Mid-Range': pricing_data['locality_adjustments']['Mid-Range'] * city_data['base_price_per_sqft'],
                'Budget': pricing_data['locality_adjustments']['Budget'] * city_data['base_price_per_sqft']
            },
            'demand_score': 85 if city_data['tier'] == 1 else 70 
        }
        return jsonify(insights)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/investment_hotspots')
def investment_hotspots():
    # Simulated hotspots based on growth potential
    hotspots = [
        {"city": "Hyderabad", "growth": "18.5%", "reason": "IT Expansion & Metro connectivity", "status": "🔥 Very High"},
        {"city": "Pune", "growth": "15.2%", "reason": "Manufacturing Hub & Residential Demand", "status": "📈 High"},
        {"city": "Ahmedabad", "growth": "14.1%", "reason": "Infrastructure growth & GIFT city", "status": "✨ Rising"},
        {"city": "Bangalore", "growth": "12.8%", "reason": "Steady IT demand & New Airport Road", "status": "✅ Stable"},
        {"city": "Guwahati", "growth": "11.5%", "reason": "Northeast regional hub development", "status": "🚀 Emerging"}
    ]
    return jsonify(hotspots)

@app.route('/api/market_trends/<city>')
def market_trends(city):
    # Simulated 5-year price trend data
    years = ["2022", "2023", "2024", "2025", "2026 (Est)"]
    
    # Base prices for simulation
    base_trend_multiplier = {
        "Mumbai": [15000, 16200, 17100, 18000, 19200],
        "Delhi NCR": [11000, 11800, 12500, 13400, 14500],
        "Bangalore": [8500, 9200, 10100, 11200, 12500],
        "Hyderabad": [6500, 7200, 8100, 9500, 11000],
        "Chennai": [7800, 8300, 8900, 9600, 10500],
        "Pune": [7200, 7800, 8500, 9400, 10800],
        "Kolkata": [6200, 6500, 6900, 7400, 8200],
        "Ahmedabad": [5500, 5900, 6500, 7300, 8100]
    }
    
    trends = base_trend_multiplier.get(city, [5000, 5300, 5700, 6200, 6800])
    
    return jsonify({
        "labels": years,
        "values": trends
    })

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
