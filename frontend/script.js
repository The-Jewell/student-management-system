//setup request for CRUD
function fetchData(url, method = 'GET', data = null){
    const options = {
        method: method, 
        headers: {
            'Content-Type': 'application/json'
        }
    };
    if(data){
        options.body = JSON.stringify(data);
    }
    return fetch(url, options).then(response => response.json());
}

//load and display all students 
function loadStudents(){
    fetchData('/students')
        .then(data => {
            console.log(data);  // Log student data
            const tableBody = document.getElementById('student-table').getElementsByTagName('tbody')[0];
            tableBody.innerHTML = ''; // Clear existing entries
            data.forEach(student => {
                let row = tableBody.insertRow();
                row.innerHTML =` 
                    <td>${student.name}</td>
                    <td>${student.dateOfBirth}</td>
                    <td>${student.grade}</td>
                    <td>${student.email}</td>
                    <td>
                        <button onclick="editStudent('${student.id}')">Edit</button>
                        <button onclick="deleteStudent('${student.id}')">Delete</button>
                    </td>
                `;
            });
        })
        .catch(error => console.error('Error loading the students:', error));
}

//collect data from form and handle create/update
function submitStudent(){
    const studentName = document.getElementById('name').value;
    const studentDOB = document.getElementById('dateOfBirth').value;
    const studentGrade = document.getElementById('grade').value;
    const studentEmail = document.getElementById('email').value;

    const studentData = {
        name: studentName,
        dateOfBirth: studentDOB,
        grade: studentGrade,
        email: studentEmail
    };
    addOrUpdateStudent(studentData);
}

//add or update student in backend
function addOrUpdateStudent(student){
    const method = student.id ? 'PUT' : 'POST';
    const url = student.id ? `/students/${student.id}` : '/students';
    fetchData(url, method, student)
        .then(() => loadStudents())
        .catch(error => console.error('Error saving the student:', error));
}

//delete student 
function deleteStudent(studentId) {
    fetch(`/students/${studentId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);  // Display success message from server
        loadStudents();  // Reload the list of students
    })
    .catch(error => console.error('Error deleting the student:', error));
}

function editStudent(studentId) {
    console.log("Edit student called with ID:", studentId);  // This should log the ID
    fetchData('/students')
        .then(students => {
            const student = students.find(s => s.id === studentId);
            if (student) {
                document.getElementById('editId').value = student.id;
                document.getElementById('editName').value = student.name;
                document.getElementById('editDateOfBirth').value = student.dateOfBirth;
                document.getElementById('editGrade').value = student.grade;
                document.getElementById('editEmail').value = student.email;
                document.getElementById('editForm').style.display = 'block'; // Show the form
            } else {
                console.error('Student not found with ID:', studentId);
            }
        })
        .catch(error => console.error('Error fetching students:', error));
}

function updateStudent() {
    const studentId = document.getElementById('editId').value;  // Ensure this is captured as a string
    const studentData = {
        id: studentId,  // Already a string from input
        name: document.getElementById('editName').value,
        dateOfBirth: document.getElementById('editDateOfBirth').value,
        grade: document.getElementById('editGrade').value,
        email: document.getElementById('editEmail').value,
    };
    fetchData(`/students/${studentId}`, 'PUT', studentData)
        .then(() => {
            loadStudents();  // Reload the student list
            document.getElementById('editForm').style.display = 'none'; // Hide the form
        })
        .catch(error => console.error('Error updating the student:', error));
}

//document ready event
document.addEventListener('DOMContentLoaded', function(){
    loadStudents();
});
