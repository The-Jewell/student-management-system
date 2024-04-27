import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from server import app  
import json

def get_data_filename():
    """Function to get the filename based on the environment."""
    test_env = os.environ.get('TESTING')
    return 'backend/students_test.json' if test_env else 'backend/students.json'

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Save the current state before the test
    with open(get_data_filename(), 'r') as file:
        original_data = json.load(file)

    with app.test_client() as client:
        yield client

    # Restore the original data after the test
    with open(get_data_filename(), 'w') as file:
        json.dump(original_data, file, indent=4)

def test_home_page(client):
    """Test that the home page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200

def test_get_students(client):
    """Test retrieving students"""
    response = client.get('/students')
    assert response.status_code == 200
    
    # Load response data as JSON
    students = response.get_json()
    assert students
    assert any(student['name'] == 'Alice Johnson' for student in students)

def test_create_student(client):
    """Test creating a new student"""
    new_student = {
        "name": "John Doe",
        "dateOfBirth": "1990-01-01",
        "grade": "A",
        "email": "john.doe@example.com"
    }
    response = client.post('/students', json=new_student)
    assert response.status_code == 201
    assert response.json['id'] is not None
    assert response.json['name'] == "John Doe"

def test_update_student(client):
    """Test updating an existing student"""
    updates = {"grade": "A+", "email": "updated@example.com"}
    response = client.put('/students/1', json=updates)
    assert response.status_code == 200
    assert response.json['message'] == 'Student updated successfully'

def test_delete_student(client):
    """Test deleting a student"""
    response = client.delete('/students/1')
    assert response.status_code == 200
    assert response.json['message'] == 'Student deleted successfully'
