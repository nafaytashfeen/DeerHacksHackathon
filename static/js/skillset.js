document.addEventListener("DOMContentLoaded", function () {
    const submitButton = document.getElementById("submit-button");

    submitButton.addEventListener("click", function (event) {
        event.preventDefault(); // Prevent form submission reload

        // Get skill inputs
        const skill1 = document.getElementById("f1").value.trim();
        const skill2 = document.getElementById("f1.2").value.trim();
        const skill3 = document.getElementById("f2").value.trim();

        // Ensure all skills are filled
        if (!skill1 || !skill2 || !skill3) {
            alert("Please enter all three skills.");
            return;
        }

        // Store skills in an array
        const skills = [skill1, skill2, skill3];

        // Retrieve stored user data from sessionStorage
        const userData = JSON.parse(sessionStorage.getItem("user_data"));

        if (!userData) {
            alert("User data not found. Please register again.");
            window.location.href = "register.html"; // Redirect back if data is missing
            return;
        }

        // Add skills to user data
        userData.skills = skills;

        // Send data to backend
        fetch("http://127.0.0.1:5001/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(userData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Registration successful!");
                sessionStorage.setItem("user_data"); // put user data in session storage
                window.location.href = "/index.html"; // Redirect to homepage
            } else {
                alert("Error: " + data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Something went wrong. Please try again.");
        });
    });
});
