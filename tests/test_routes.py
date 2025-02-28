"""
Tests for the Healthcare Translation Web App routes.
"""
import pytest
import json
from app import create_app

@pytest.fixture
def client():
    """Create a test client for the app."""
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test that the index route returns the expected HTML."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Healthcare Translator' in response.data

def test_user_guide_route(client):
    """Test that the user guide route returns the expected HTML."""
    response = client.get('/user-guide')
    assert response.status_code == 200
    assert b'User Guide' in response.data

def test_health_check_route(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_translate_missing_data(client):
    """Test the translate endpoint rejects requests with missing data."""
    response = client.post('/api/translate', 
                          data=json.dumps({}),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_translate_missing_fields(client):
    """Test the translate endpoint rejects requests with missing required fields."""
    response = client.post('/api/translate', 
                          data=json.dumps({'text': 'Hello'}),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_text_to_speech_missing_data(client):
    """Test the text-to-speech endpoint rejects requests with missing data."""
    response = client.post('/api/text-to-speech', 
                          data=json.dumps({}),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_text_to_speech_missing_fields(client):
    """Test the text-to-speech endpoint rejects requests with missing required fields."""
    response = client.post('/api/text-to-speech', 
                          data=json.dumps({'text': 'Hello'}),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data