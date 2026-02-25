import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test if home page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Housing Price Predictor" in response.data

def test_about_page(client):
    """Test if about page loads"""
    response = client.get('/about')
    assert response.status_code == 200

def test_login_page_loading(client):
    """Test if login page loads"""
    response = client.get('/login')
    assert response.status_code == 200

def test_prediction_api_structure(client):
    """Test if the prediction logic returns 200 (even if inputs are mocked)"""
    # This is a sample form submission
    response = client.post('/', data={
        'city': 'Mumbai',
        'property_type': 'Apartment',
        'bhk': '2 BHK',
        'area_sqft': '1000',
        'locality_tier': 'Mid-Range',
        'age_of_property': 'New (0-1 year)',
        'furnishing': 'Unfurnished'
    })
    assert response.status_code == 200
