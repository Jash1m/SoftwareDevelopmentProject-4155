import pytest
from app import app, db, update_admin_credentials
from schemas.schemas import Response, Student, Period, Question

@pytest.fixture
def client():
    """Setup a Flask test client."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory SQLite database for testing
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables for the test database
            setup_test_data()  # Insert any required initial data
        yield client
        with app.app_context():
            db.drop_all()  # Clean up the database

def setup_test_data():
    """Insert initial data for testing."""
    # Add a test period
    period = Period(periodName="Test Period", numDoubles=10, numQuads=5)
    db.session.add(period)
    db.session.commit()

def test_login_valid_credentials(client):
    """Test login with valid credentials."""
    update_admin_credentials("test_user", "password123")
    response = client.post('/login', data={'username': 'test_user', 'password': 'password123'})
    assert response.status_code == 302  # Redirect after successful login
    assert response.headers['Location'] == '/'  # Ensure redirected to the index page


def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    update_admin_credentials("test_user", "password123")
    response = client.post('/login', data={'username': 'wrong_user', 'password': 'wrong_pass'})
    assert response.status_code == 200  # Stay on login page
    assert b'Login' in response.data  # Check for presence of the login form

def test_simulate_responses(client):
    """Test the simulate responses functionality."""
    # Simulate 5 responses
    response = client.post('/simulate_responses', data={'num_responses': 5})
    assert response.status_code == 302  # Redirect after processing
    
    # Verify the database has 5 new responses
    with app.app_context():
        all_responses = Response.query.all()
        assert len(all_responses) == 5

# Test for the index page (GET route)
def test_index_redirect(client):
    """Test if non-logged-in user is redirected to the login page."""
    response = client.get('/')
    assert response.status_code == 302  # Should redirect to login page
    assert response.headers['Location'] == '/login'  # Redirection location should be the login page

def test_index_logged_in(client):
    """Test if logged-in user can access the index page."""
    # Simulate a login by setting session data directly (this assumes you have session management)
    with client.session_transaction() as session:
        session['username'] = 'test_user'
    
    response = client.get('/')
    assert response.status_code == 200  # Should successfully load index page
    assert b'CHARLOTTE' in response.data  # Check for welcome message or any expected page content

# Test for the survey page (GET route)
def test_survey_redirect(client):
    """Test if non-logged-in user is redirected to the login page for survey."""
    response = client.get('/survey')
    assert response.status_code == 302  # Should redirect to login page
    assert response.headers['Location'] == '/login'  # Redirection location should be the login page

def test_survey_logged_in(client):
    """Test if logged-in user can access the survey page."""
    # Simulate a login by setting session data directly (this assumes you have session management)
    with client.session_transaction() as session:
        session['username'] = 'test_user'
    
    response = client.get('/survey')
    assert response.status_code == 200  # Should successfully load survey page
    assert b'Survey' in response.data  # Check for survey-related content

# Test for the admin page (GET route)

def test_admin_logged_in(client):
    """Test if logged-in user can access the admin page."""
    # Simulate a login by setting session data directly (this assumes you have session management)
    with client.session_transaction() as session:
        session['username'] = 'test_user'
    
    response = client.get('/admin')
    assert response.status_code == 200  # Should successfully load admin page
    assert b'CHARLOTTE' in response.data  # Check for header

def test_matching_logged_in(client):
    """Test if logged-in user can access the matching page."""
    # Simulate a login by setting session data directly (this assumes you have session management)
    with client.session_transaction() as session:
        session['username'] = 'test_user'
    
    response = client.get('/matching')
    assert response.status_code == 200  # Should successfully load matching page
    assert b'Matching' in response.data  # Check for matching-related content


def test_responses_logged_in(client):
    """Test if logged-in user can access the responses page."""
    # Simulate a login by setting session data directly (this assumes you have session management)
    with client.session_transaction() as session:
        session['username'] = 'test_user'
    
    response = client.get('/responses')
    assert response.status_code == 200  # Should successfully load responses page
    assert b'Responses' in response.data  # Check for responses-related content

def test_user_responses_route(client):
    """Test the user responses route. Simulate a POST request for survey submission."""
    data = {
        '1': 'freshman',  # Example of answers
        '2': 'Computer science',
        '3': 'yes',
        '4': '3',  # Sample answer for numeric question
        '5': '10pm',
        '6': '10pm-midnight',
        '7': 'Study Alone',
        '8': 'Reading',
        '9': 'cool',
        '10': 'tidy',
        '11': 'confront',
    }
    response = client.post('/user', data=data)
    assert response.status_code == 302  # Expecting a redirect to index page

def test_display_responses_route(client):
    """Test the route to display all responses."""
    response = client.get('/responses')
    assert response.status_code == 200
    assert b'CHARLOTTE' in response.data  # Expect to see the header

def test_simulate_responses_route(client):
    """Test the simulate responses route. Simulate POST with number of responses."""
    response = client.post('/simulate_responses', data={'num_responses': 5})
    assert response.status_code == 302  # Redirect to responses page
