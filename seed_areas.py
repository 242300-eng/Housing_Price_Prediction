from pymongo import MongoClient

def seed_city_areas():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['housing_db']
    
    # All major cities & state capitals with real locality areas
    city_areas_data = {
        # --- Tier 1 Metros ---
        "Mumbai": [
            {"name": "South Mumbai (Colaba/Malabar Hill)", "multiplier": 2.5},
            {"name": "Bandra/Juhu", "multiplier": 2.0},
            {"name": "Andheri/Borivali", "multiplier": 1.2},
            {"name": "Thane/Navi Mumbai", "multiplier": 0.8},
            {"name": "Dharavi/Kurla", "multiplier": 0.6}
        ],
        "Delhi NCR": [
            {"name": "Lutyens' Delhi", "multiplier": 2.8},
            {"name": "South Delhi (Greater Kailash)", "multiplier": 1.8},
            {"name": "Gurugram Phase 1-5", "multiplier": 1.5},
            {"name": "Noida Extension", "multiplier": 0.7},
            {"name": "Old Delhi", "multiplier": 0.9}
        ],
        "Bangalore": [
            {"name": "Indiranagar/Koramangala", "multiplier": 1.7},
            {"name": "Whitefield/ITPL", "multiplier": 1.3},
            {"name": "Electronic City", "multiplier": 0.9},
            {"name": "Hebbal/Manyata", "multiplier": 1.2},
            {"name": "Mysore Road", "multiplier": 0.7}
        ],
        "Hyderabad": [
            {"name": "Banjara Hills/Jubilee Hills", "multiplier": 2.2},
            {"name": "Hitech City/Gachibowli", "multiplier": 1.4},
            {"name": "Kukatpally", "multiplier": 0.9},
            {"name": "Secunderabad", "multiplier": 0.8},
            {"name": "Uppal", "multiplier": 0.6}
        ],
        "Chennai": [
            {"name": "Poes Garden/Boat Club", "multiplier": 2.4},
            {"name": "Adyar/Besant Nagar", "multiplier": 1.6},
            {"name": "OMR/IT Corridor", "multiplier": 1.1},
            {"name": "Ambattur", "multiplier": 0.7},
            {"name": "Tambaram", "multiplier": 0.6}
        ],
        "Pune": [
            {"name": "Koregaon Park/Kalyani Nagar", "multiplier": 1.9},
            {"name": "Hinjewadi IT Park", "multiplier": 1.2},
            {"name": "Baner/Aundh", "multiplier": 1.3},
            {"name": "Hadapsar/Wagholi", "multiplier": 0.8},
            {"name": "Pimpri-Chinchwad", "multiplier": 0.7}
        ],

        # --- State Capitals ---
        # Andhra Pradesh - Amaravati / Vijayawada
        "Vijayawada": [
            {"name": "Benz Circle", "multiplier": 1.5},
            {"name": "Governorpet", "multiplier": 1.3},
            {"name": "Moghalrajpuram", "multiplier": 1.0},
            {"name": "Patamata", "multiplier": 0.8},
            {"name": "Nunna/AP Capital Region", "multiplier": 0.7}
        ],
        # Arunachal Pradesh
        "Itanagar": [
            {"name": "Naharlagun", "multiplier": 1.2},
            {"name": "Ganga Market", "multiplier": 1.0},
            {"name": "Nirjuli", "multiplier": 0.8},
            {"name": "Banderdewa", "multiplier": 0.7}
        ],
        # Assam
        "Guwahati": [
            {"name": "Paltan Bazaar/Pan Bazaar", "multiplier": 1.6},
            {"name": "Beltola/Zoo Road", "multiplier": 1.2},
            {"name": "Guwahati Medical College Area", "multiplier": 1.0},
            {"name": "Jalukbari", "multiplier": 0.9},
            {"name": "Khanapara", "multiplier": 0.8}
        ],
        # Bihar
        "Patna": [
            {"name": "Kurji/Kankarbagh", "multiplier": 1.5},
            {"name": "Boring Road/Ashok Rajpath", "multiplier": 1.3},
            {"name": "Rajendra Nagar", "multiplier": 1.0},
            {"name": "Danapur", "multiplier": 0.8},
            {"name": "Phulwari Sharif", "multiplier": 0.6}
        ],
        # Chhattisgarh
        "Raipur": [
            {"name": "Shankar Nagar", "multiplier": 1.5},
            {"name": "Civil Lines/Pachpedi Naka", "multiplier": 1.3},
            {"name": "Amanaka", "multiplier": 1.0},
            {"name": "Naya Raipur", "multiplier": 1.2},
            {"name": "Durg/Bhilai", "multiplier": 0.7}
        ],
        # Goa
        "Panaji": [
            {"name": "Panaji City Centre", "multiplier": 2.0},
            {"name": "Porvorim", "multiplier": 1.5},
            {"name": "Panjim/Altinho", "multiplier": 1.8},
            {"name": "Calangute/Candolim", "multiplier": 1.3},
            {"name": "Margao", "multiplier": 0.9}
        ],
        # Gujarat
        "Ahmedabad": [
            {"name": "SG Highway/Prahlad Nagar", "multiplier": 1.7},
            {"name": "Bopal/South Bopal", "multiplier": 1.2},
            {"name": "CG Road/Navrangpura", "multiplier": 1.5},
            {"name": "Vastral/Narol", "multiplier": 0.7},
            {"name": "Nikol/Gota", "multiplier": 0.8}
        ],
        # Haryana
        "Chandigarh": [
            {"name": "Sector 17/22 (Main City)", "multiplier": 2.0},
            {"name": "Sector 70-82 (Sahibzada Ajit Singh Nagar)", "multiplier": 1.3},
            {"name": "Panchkula Sectors", "multiplier": 1.0},
            {"name": "Industrial Area Phase 1/2", "multiplier": 0.8},
            {"name": "Mullanpur New Chandigarh", "multiplier": 0.9}
        ],
        # Himachal Pradesh
        "Shimla": [
            {"name": "Mall Road/Ridge", "multiplier": 2.2},
            {"name": "Sanjauli", "multiplier": 1.3},
            {"name": "Kamla Nagar/Kasumpti", "multiplier": 1.0},
            {"name": "Vikas Nagar", "multiplier": 0.8},
            {"name": "Shoghi/Outskirts", "multiplier": 0.6}
        ],
        # Jharkhand
        "Ranchi": [
            {"name": "Harmu/Kanke Road", "multiplier": 1.5},
            {"name": "Doranda", "multiplier": 1.2},
            {"name": "Lalpur", "multiplier": 1.0},
            {"name": "Namkum/Tatisilwai", "multiplier": 0.7},
            {"name": "Sukhdeonagar", "multiplier": 0.8}
        ],
        # Karnataka (Bangalore already listed)
        # Kerala
        "Thiruvananthapuram": [
            {"name": "Kowdiar/Vazhuthacaud", "multiplier": 1.8},
            {"name": "Pattom/Kesavadasapuram", "multiplier": 1.4},
            {"name": "Vanchiyoor/Palayam", "multiplier": 1.1},
            {"name": "Kazhakkoottam/Technopark", "multiplier": 1.0},
            {"name": "Attingal/Neyyattinkara", "multiplier": 0.6}
        ],
        # Madhya Pradesh
        "Bhopal": [
            {"name": "Arera Colony", "multiplier": 1.7},
            {"name": "MP Nagar/New Market", "multiplier": 1.4},
            {"name": "Kolar Road", "multiplier": 1.0},
            {"name": "Govindpura", "multiplier": 0.8},
            {"name": "Bairagarh", "multiplier": 0.6}
        ],
        # Maharashtra (Mumbai, Pune already listed)
        "Nagpur": [
            {"name": "Civil Lines/Dharampeth", "multiplier": 1.6},
            {"name": "Wardha Road/Automotive Square", "multiplier": 1.2},
            {"name": "Nandanvan/Manish Nagar", "multiplier": 1.0},
            {"name": "Hingna/MIHAN", "multiplier": 0.8},
            {"name": "Kamptee Road", "multiplier": 0.7}
        ],
        # Manipur
        "Imphal": [
            {"name": "Imphal City Centre", "multiplier": 1.3},
            {"name": "Thangmeiband", "multiplier": 1.0},
            {"name": "Keishamthong", "multiplier": 0.9},
            {"name": "Lamphel", "multiplier": 0.8},
            {"name": "Porompat/Outskirts", "multiplier": 0.6}
        ],
        # Meghalaya
        "Shillong": [
            {"name": "Police Bazaar/Laitumkhrah", "multiplier": 1.7},
            {"name": "Rynjah/Nongthymmai", "multiplier": 1.1},
            {"name": "Mawlai", "multiplier": 0.9},
            {"name": "Umiam/Barapani", "multiplier": 0.7}
        ],
        # Mizoram
        "Aizawl": [
            {"name": "Bawngkawn", "multiplier": 1.2},
            {"name": "Ramhlun/Zarkawt", "multiplier": 1.0},
            {"name": "Chaltlang", "multiplier": 0.9},
            {"name": "Electric Veng", "multiplier": 0.8}
        ],
        # Nagaland
        "Kohima": [
            {"name": "Kohima Town", "multiplier": 1.2},
            {"name": "Dimapur/Industrial Area", "multiplier": 1.0},
            {"name": "Razhu Point", "multiplier": 0.9},
            {"name": "Outskirts", "multiplier": 0.7}
        ],
        # Odisha
        "Bhubaneswar": [
            {"name": "Jaydev Vihar/Nayapalli", "multiplier": 1.7},
            {"name": "Infocity/Patia", "multiplier": 1.3},
            {"name": "Chandrasekharpur", "multiplier": 1.1},
            {"name": "Master Canteen/Saheed Nagar", "multiplier": 1.0},
            {"name": "Aiginia/Jatni", "multiplier": 0.7}
        ],
        # Punjab
        "Amritsar": [
            {"name": "Golden Temple Area/Lawrence Road", "multiplier": 1.5},
            {"name": "Ranjit Avenue", "multiplier": 1.3},
            {"name": "GT Road Corridor", "multiplier": 1.0},
            {"name": "Airport Road", "multiplier": 0.8},
            {"name": "Outskirts", "multiplier": 0.6}
        ],
        # Rajasthan
        "Jaipur": [
            {"name": "Malviya Nagar/Vaishali Nagar", "multiplier": 1.5},
            {"name": "C-Scheme/Civil Lines", "multiplier": 1.8},
            {"name": "Jagatpura/Sitapura", "multiplier": 1.0},
            {"name": "Sanganer", "multiplier": 0.8},
            {"name": "Ajmer Road", "multiplier": 0.7}
        ],
        # Sikkim
        "Gangtok": [
            {"name": "MG Marg/Main Market", "multiplier": 1.5},
            {"name": "Tadong", "multiplier": 1.0},
            {"name": "Ranipool", "multiplier": 0.8},
            {"name": "Singtam/Outskirts", "multiplier": 0.6}
        ],
        # Tamil Nadu (Chennai already listed)
        "Coimbatore": [
            {"name": "Avinashi Road/Peelamedu", "multiplier": 1.4},
            {"name": "Gandhipuram/RS Puram", "multiplier": 1.2},
            {"name": "Tidel Park/Coimbatore IT Hub", "multiplier": 1.3},
            {"name": "Saravanampatty", "multiplier": 1.0},
            {"name": "Kovaipudur", "multiplier": 0.8}
        ],
        # Telangana (Hyderabad already listed)
        # Tripura
        "Agartala": [
            {"name": "Agartala City Centre", "multiplier": 1.3},
            {"name": "Battala/VIP Road", "multiplier": 1.0},
            {"name": "Badharghat", "multiplier": 0.9},
            {"name": "Indranagar", "multiplier": 0.8},
            {"name": "Outskirts", "multiplier": 0.6}
        ],
        # Uttar Pradesh
        "Lucknow": [
            {"name": "Gomti Nagar/Vibhuti Khand", "multiplier": 1.6},
            {"name": "Hazratganj/Civil Lines", "multiplier": 1.4},
            {"name": "Alambagh/Charbagh", "multiplier": 1.0},
            {"name": "Mahanagar/Aliganj", "multiplier": 1.1},
            {"name": "Kanpur Road", "multiplier": 0.7}
        ],
        # Uttarakhand
        "Dehradun": [
            {"name": "Rajpur Road/ISBT", "multiplier": 1.5},
            {"name": "Saharanpur Road/Dharampur", "multiplier": 1.2},
            {"name": "Vasant Vihar/Hathibarkala", "multiplier": 1.3},
            {"name": "Prem Nagar/Sahaspur", "multiplier": 0.8},
            {"name": "Haridwar Road", "multiplier": 0.7}
        ],
        # West Bengal
        "Kolkata": [
            {"name": "Salt Lake City/Sector V", "multiplier": 1.6},
            {"name": "Ballygunge/Alipore", "multiplier": 2.0},
            {"name": "New Town/Rajarhat", "multiplier": 1.2},
            {"name": "Howrah/Liluah", "multiplier": 0.8},
            {"name": "Dunlop/Nager Bazar", "multiplier": 0.7}
        ],
        # J&K
        "Srinagar": [
            {"name": "Dal Lake/Boulevard Road", "multiplier": 1.8},
            {"name": "Rajbagh/Jawahar Nagar", "multiplier": 1.5},
            {"name": "Bemina", "multiplier": 1.0},
            {"name": "Soura/Rangreth", "multiplier": 0.8},
            {"name": "Outer Srinagar", "multiplier": 0.6}
        ],
        # Ladakh
        "Leh": [
            {"name": "Leh Market/Old Town", "multiplier": 1.5},
            {"name": "Changspa", "multiplier": 1.2},
            {"name": "Sheynam Road", "multiplier": 0.9},
            {"name": "Choglamsar", "multiplier": 0.8}
        ],
    }

    print("Updating city areas in MongoDB...")
    updated = 0
    for city_name, areas in city_areas_data.items():
        result = db.cities.update_one(
            {"name": city_name},
            {"$set": {"areas": areas}}
        )
        if result.matched_count:
            print(f"  [DONE] Updated {city_name} with {len(areas)} areas.")
            updated += 1
        else:
            print(f"  [MISSING] City not found in DB: {city_name}")

    # Add default areas for any other city not explicitly listed
    default_areas = [
        {"name": "City Centre / Prime", "multiplier": 1.4},
        {"name": "Main City / Residential", "multiplier": 1.0},
        {"name": "Suburban / Developing", "multiplier": 0.8},
        {"name": "Outskirts / Affordable", "multiplier": 0.6}
    ]
    
    db.cities.update_many(
        {"name": {"$nin": list(city_areas_data.keys())}},
        {"$set": {"areas": default_areas}}
    )
    print(f"\nDone! {updated} cities updated with specific areas.")
    print("All other cities got default 4-zone areas.")

if __name__ == "__main__":
    seed_city_areas()
