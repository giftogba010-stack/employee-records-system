const employeeList = document.getElementById("employee-list");
const addButton = document.querySelector(".add-btn");
const formContainer = document.getElementById("employee-form");

addButton.addEventListener("click", function () {
    formContainer.innerHTML = `
        <form id="employeeForm">
            <input type="text" id="fullName" placeholder="Full Name" required>
            <input type="email" id="email" placeholder="Email" required>
            <input type="text" id="department" placeholder="Department" required>
            <input type="text" id="jobTitle" placeholder="Job Title" required>
            <button type="submit">Submit</button>
        </form>
    `;

    const employeeForm = document.getElementById("employeeForm");

    employeeForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const newEmployee = document.createElement("div");
        newEmployee.className = "employee";

        newEmployee.innerHTML = `
            <h3>${document.getElementById("fullName").value}</h3>
            <p>${document.getElementById("jobTitle").value}</p>
            <p>${document.getElementById("department").value}</p>
            <p>${document.getElementById("email").value}</p>
            <button type="button" class="remove-btn">Remove</button>
        `;

        employeeList.appendChild(newEmployee);

        newEmployee.querySelector(".remove-btn").addEventListener("click", function () {
            newEmployee.remove();
        });

        employeeForm.reset();
    });
});