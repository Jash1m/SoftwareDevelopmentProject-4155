import pytest
from app import app, db, Response

# This fixture creates a test client and sets up the application context for testing
@pytest.fixture
def client():
    # Set the test configuration
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
    with app.app_context():
        db.create_all()  # Create the database and the tables
        yield app.test_client()  # Provide the test client
        db.drop_all()  # Clean up after tests

# Test the index route
def test_index(client):
    response = client.get('/')  # Send a GET request to the index route
    assert response.status_code == 200  # Check if the status code is 200
    assert b'Welcome' in response.data  # Ensure the expected content is in the response (you can change 'Welcome' to any expected content in your index.html)

# Test the survey route
def test_survey(client):
    response = client.get('/survey')  # Send a GET request to the survey route
    assert response.status_code == 200  # Check if the status code is 200
    assert b'Survey' in response.data  # Ensure the expected content is in the response (you can change 'Survey' to any expected content in your survey.html)
