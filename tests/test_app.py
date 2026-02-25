import pytest

# Try to import, but gracefully handle if MongoDB isn't available
try:
    from app import app as flask_app, db
    MONGO_AVAILABLE = True
except Exception:
    MONGO_AVAILABLE = False
    flask_app = None

@pytest.fixture
def client():
    if not MONGO_AVAILABLE or flask_app is None:
        pytest.skip("MongoDB not available")
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_home_page(client):
    """Test if home page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200

def test_about_page(client):
    """Test if about page loads"""
    response = client.get('/about')
    assert response.status_code == 200

def test_login_page_loading(client):
    """Test if login page loads"""
    response = client.get('/login')
    assert response.status_code == 200

def test_prediction_form_submission(client):
    """Test prediction form returns 200"""
    response = client.post('/', data={
        'city': 'Mumbai',
        'property_type': 'Apartment',
        'bhk': '2 BHK',
        'area_sqft': '1000',
        'locality_tier': 'Mid-Range',
        'age_of_property': 'New (0-1 year)',
        'furnishing': 'Unfurnished',
        'area_multiplier': '1.0'
    })
    assert response.status_code == 200
