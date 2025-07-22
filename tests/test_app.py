import pytest
from app import app, hashing_pass
import os 
import re 

def test_app_routes():
    app.config['TESTING'] = True
    client = app.test_client()

    # test home page
    response = client.get('/')
    assert response.status_code == 200

    # test information page
    response = client.get('/information')
    assert response.status_code == 200

    # test login page
    response = client.get('/login')
    assert response.status_code == 200

    # test signup page
    response = client.get('/signup')
    assert response.status_code == 200

# test incorrect login details
def test_invalid_login():
    os.system('python create_dbs.py')
    app.config['TESTING'] = True
    client = app.test_client()

    response = client.post('/login', data={
        'username': 'testaccount',
        'password': 'WinstoN!1'
    }, follow_redirects=True)

    assert b"Invalid username or password." in response.data

# test medical records page requires user to be logged in 
def test_medical_requires_login():
    app.config['TESTING'] = True
    client = app.test_client()

    response = client.get('/medical_records', follow_redirects=False)
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

# test predictor page requires user to be logged in 
def test_predictor_requires_login():
    app.config['TESTING'] = True
    client = app.test_client()

    response = client.get('/predictor', follow_redirects=False)
    assert response.status_code == 302
    assert '/login' in response.headers['Location']   

# test logging out of account
def test_logout():
    app.config['TESTING'] = True
    client = app.test_client()

    with client.session_transaction() as session:
        session['user_id'] = -1
        session['username'] = 'testaccount'

    response = client.get('/logout', follow_redirects=True)
    assert b"Log In" in response.data or response.status_code == 200

# test hashing of password
def test_password_hashing():
    password = 'WinstoN!1'
    hashed = hashing_pass(password)

    assert hashed != password  # Ensure password is not stored as plain text
    assert len(hashed) == 64

# test password requirements
def test_password_requirements():
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%&*\\-])[A-Za-z\d!@#$%&*\\-]{8,}$'

    # Valid password
    assert re.match(password_regex, 'WinstoN!1')

    # Too short
    assert not re.match(password_regex, 'Wins!1')

    # Missing special character
    assert not re.match(password_regex, 'Winston1')

    # Missing uppercase
    assert not re.match(password_regex, 'winston!1')

    # Missing digit
    assert not re.match(password_regex, 'Winston!')
    
