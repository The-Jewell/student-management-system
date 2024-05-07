import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from server import app, Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from server import Base, DATABASE_URI

# Set up a test database URI if needed, or use the same if isolation is handled via transactions
TEST_DATABASE_URI = DATABASE_URI

@pytest.fixture(scope='module')
def test_client():
    # Configure the app to use the testing configuration
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI

    # Create the test database structure
    engine = create_engine(TEST_DATABASE_URI)
    Base.metadata.create_all(engine)

    # Establish an application context before running the tests
    testing_client = app.test_client()

    # Context manager to manage the lifecycle of the session
    ctx = app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()

    # Drop all to clean up the test database
    Base.metadata.drop_all(engine)

@pytest.fixture(autouse=True)
def session():
    """Create a scoped session for database transactions."""
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=create_engine(TEST_DATABASE_URI)))
    yield session
    session.rollback()
    session.close()

def test_home_page(test_client):
    """Test that the home page loads correctly."""
    response = test_client.get('/')
    assert response.status_code == 200

def test_get_students(test_client, session):
    """Test retrieving students."""
    response = test_client.get('/students')
    assert response.status_code == 200
    students = response.get_json()
    assert isinstance(students, list)

def test_create_student(test_client, session):
    """Test creating a new student."""
    new_student = {
        "name": "John Doe",
        "dateOfBirth": "1990-01-01",
        "grade": "A",
        "email": "john.doe@example.com"
    }
    response = test_client.post('/students', json=new_student)
    assert response.status_code == 201
    student_data = response.get_json()
    assert student_data['id'] is not None
    assert student_data['name'] == "John Doe"

def test_update_student(test_client, session):
    """Test updating an existing student."""
    updates = {"grade": "A+", "email": "updated@example.com"}
    response = test_client.put('/students/1', json=updates)
    assert response.status_code == 200
    updated_data = response.get_json()
    assert updated_data['message'] == 'Student updated successfully'

def test_delete_student(test_client, session):
    """Test deleting a student."""
    response = test_client.delete('/students/1')
    assert response.status_code == 200
    deleted_data = response.get_json()
    assert deleted_data['message'] == 'Student deleted successfully'
