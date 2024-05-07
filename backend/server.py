from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError

import os

# Database setup
DATABASE_URI = 'postgresql+psycopg2://my_user:my_password@localhost/student_management'
engine = create_engine(DATABASE_URI, echo=True)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
Base = declarative_base()

# Define model
class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    date_of_birth = Column(Date)
    grade = Column(String)
    email = Column(String)

    def __repr__(self):
        return f"<Student(name={self.name}, email={self.email})>"

app = Flask(__name__, static_folder='../frontend', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/students', methods=['GET'])
def get_students():
    session = Session()
    try:
        students = session.query(Student).all()
        student_list = [{'id': student.id, 'name': student.name, 'dateOfBirth': student.date_of_birth, 'grade': student.grade, 'email': student.email} for student in students]
        print("Fetched students:", student_list)  # Debugging line to check what's fetched
        return jsonify(student_list)
    except Exception as e:
        session.rollback()
        print("Error fetching students:", str(e))  # Log the error
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@app.route('/students', methods=['POST'])
def create_student():
    student_data = request.get_json()
    try:
        new_student = Student(
            name=student_data.get('name'),
            date_of_birth=student_data.get('dateOfBirth'),  # Store as-is
            grade=student_data.get('grade'),
            email=student_data.get('email')
        )
        
        session = Session()
        session.add(new_student)
        session.commit()

        # Return the student data directly, keeping date_of_birth as provided
        return jsonify({
            'id': new_student.id,
            'name': new_student.name,
            'dateOfBirth': new_student.date_of_birth,  # Directly return as-is
            'grade': new_student.grade,
            'email': new_student.email
        }), 201

    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    session = Session()
    student = session.query(Student).filter(Student.id == student_id).one_or_none()
    if student is None:
        session.close()
        return jsonify({'message': 'Student not found'}), 404
    
    student_data = request.get_json()
    student.name = student_data.get('name', student.name)
    student.date_of_birth = student_data.get('dateOfBirth', student.date_of_birth)
    student.grade = student_data.get('grade', student.grade)
    student.email = student_data.get('email', student.email)
    session.commit()
    session.close()
    return jsonify({'message': 'Student updated successfully'}), 200

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    session = Session()
    student = session.query(Student).filter(Student.id == student_id).one_or_none()
    if student is None:
        session.close()
        return jsonify({'message': 'Student not found'}), 404
    
    session.delete(student)
    session.commit()
    session.close()
    return jsonify({'message': 'Student deleted successfully'}), 200

@app.teardown_appcontext
def remove_session(*args, **kwargs):
    Session.remove()

# Initialize database tables
Base.metadata.create_all(engine)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
