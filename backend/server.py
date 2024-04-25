from flask import Flask, request, jsonify
import json
import os

print("Current Working Directory:", os.getcwd())

app = Flask(__name__, static_folder='../frontend', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

def load_students():
    """Load Students from JSON and treat IDs as strings."""
    try:
        with open('backend/students.json', 'r') as file:
            students = json.load(file)
            # Ensure all IDs are strings
            for student in students:
                student['id'] = str(student['id'])
            print("Loaded students:", students)
            return students
    except FileNotFoundError:
        print("students.json file not found, returning empty list.")
        return []
    except json.JSONDecodeError as e:
        print("Error decoding JSON, returning empty list:", str(e))
        return []
    
def save_students(students):
    with open('backend/students.json', 'w') as file:
        json.dump(students, file, indent=4)

@app.route('/students', methods=['GET', 'POST'])
def manage_students():
    if request.method == 'GET':
        students = load_students()
        return jsonify(students)
    elif request.method == 'POST':
        student_data = request.get_json()
        students = load_students()
        if students:
            max_id = max(student['id'] for student in students)
            student_data['id'] = str(int(max_id) + 1)  # Generate next ID as string
        else:
            student_data['id'] = '1'  # Start IDs from '1' if list is empty
        students.append(student_data)
        save_students(students)
        return jsonify(student_data), 201

@app.route('/students/<student_id>', methods=['DELETE', 'PUT'])
def manage_student(student_id):
    students = load_students()
    student_data = request.get_json() if request.method == 'PUT' else None
    student_found = None
    for student in students:
        if student['id'] == student_id:
            if request.method == 'PUT':
                student.update(student_data)
            student_found = student
            break
    if not student_found:
        return jsonify({'message': 'Student not found'}), 404
    if request.method == 'PUT':
        save_students(students)
        return jsonify({'message': 'Student updated successfully'}), 200
    elif request.method == 'DELETE':
        students = [student for student in students if student['id'] != student_id]
        save_students(students)
        return jsonify({'message': 'Student deleted successfully'}), 200

if __name__ == '__main__':
    app.run(port=8000, debug=True)
