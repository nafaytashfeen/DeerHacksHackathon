document.addEventListener("DOMContentLoaded", function () {
    const submitButton = document.getElementById("submit-button");
    sessionStorage.setItem("signed_in", JSON.stringify(false))
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
        const userData = JSON.parse(sessionStorage.getItem("user_data_unverified"));

        if (!userData) {
            alert("User data not found. Please register again.");
            window.location.href = "register.html"; // Redirect back if data is missing
            return;
        }

        // Add skills to user data
        userData.skills = skills;

        // Send data to backend
        fetch("/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(userData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                user_data = {
                    "username": data.name,
                    "skill_set": data.skills
                }
                sessionStorage.setItem("user_data", JSON.stringify(user_data)); // put user data in session storage
                sessionStorage.setItem("signed_in", JSON.stringify(true))
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
