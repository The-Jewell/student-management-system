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
            const tableBody = document.getElementById('student-table').getElementsByTagName('tbody')[0];
            tableBody.innerHTML = ''; //clears existing entries
            data.forEach(student => {
                let row = tableBody.insertRow();
                row.innerHTML =` 
                    <td>${student.name}</td>
                    <td>${student.dateOfBirth}</td>
                    <td>${student.grade}</td>
                    <td>${student.email}</td>
                    <td>
                        <button onclick="editStudent(${student.id})">Edit</button>
                        <button onclick="deleteStudent(${student.id})">Delete</button>
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
    const method = student.id ? 'PUT': 'POST';
    const url = student.id ? `/students/${student.id}` : '/students';
    fetchData(url, method, student)
        .then(() => loadStudents())
        .catch(error => console.error('Error saving the student:', error));

}

//document ready event
document.addEventListener('DOMContentLoaded', function(){
    loadStudents();
});

