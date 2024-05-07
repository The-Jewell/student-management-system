# import_json_to_db.py

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
from datetime import datetime

# Database setup
DATABASE_URI = 'postgresql+psycopg2://my_user:my_password@localhost/student_management'
engine = create_engine(DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define the Student model
class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    date_of_birth = Column(Date)
    grade = Column(String)
    email = Column(String)

# Create database tables if they don't exist
Base.metadata.create_all(engine)

# Function to load data from JSON and insert into the database
def load_and_insert_data(json_path):
    # Open and load JSON file data
    with open(json_path, 'r') as file:
        students_data = json.load(file)

    # Create a session
    session = Session()

    # Iterate over each student in the JSON data
    for student_data in students_data:
        new_student = Student(
            name=student_data['name'],
            date_of_birth=datetime.strptime(student_data['dateOfBirth'], '%Y-%m-%d').date(),
            grade=student_data['grade'],
            email=student_data['email']
        )
        # Add the new student to the session
        session.add(new_student)

    # Commit the session to save all students into the database
    session.commit()
    # Close the session
    session.close()

# Path to the JSON file
json_file_path = 'students.json'

# Call the function to load and insert data
load_and_insert_data(json_file_path)
