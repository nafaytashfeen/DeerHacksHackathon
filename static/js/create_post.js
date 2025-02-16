document.addEventListener("DOMContentLoaded", function () {
    const skillSet = JSON.parse(sessionStorage.getItem("skill_set")); // Retrieve user's skills from sessionStorage
    const dropdownTeach = document.getElementById("dropdown-teach");

    if (skillSet && skillSet.length > 0) {
        // Clear existing options
        dropdownTeach.innerHTML = "";

        // Add a default option
        const defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.textContent = "Select a skill";
        dropdownTeach.appendChild(defaultOption);

        // Populate dropdown with user's skills
        skillSet.forEach(skill => {
            const option = document.createElement("option");
            option.value = skill;
            option.textContent = skill;
            dropdownTeach.appendChild(option);
        });
    } else {
        // If no skills are found, disable the dropdown
        dropdownTeach.innerHTML = '<option value="">No skills available</option>';
        dropdownTeach.disabled = true;
    }
});

document.getElementById('post-image-upload').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const preview = document.getElementById('image-preview');
            preview.src = e.target.result;
            preview.style.display = 'block'; // Reveal the preview image
        };
        reader.readAsDataURL(file);
    }
});

// this displays "signed in as {username}" in the navbar
document.addEventListener("DOMContentLoaded", () => {
    // Retrieve username from sessionStorage, default to "Guest"
    const username = sessionStorage.getItem("username") || "Guest";

    // Insert "Signed in as {username}" text in the header
    const signedInText = document.getElementById("signed-in-text");
    if (signedInText) {
        signedInText.textContent = `Signed in as ${username}`;
    }
});

document.addEventListener("DOMContentLoaded", () => {
    // Retrieve username from sessionStorage
    const username = sessionStorage.getItem("username") || "Default";
    
    // Set the text content of the poster-name element
    document.getElementById("poster-name").innerHTML = `<strong>Posted By:</strong> ${username}`;
});

document.addEventListener("DOMContentLoaded", function () {
    // Variable to hold the Base64-encoded image data
    let uploadedImageBase64 = "";

    // Handle image upload and preview
    const imageInput = document.getElementById("post-image-upload");
    imageInput.addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                uploadedImageBase64 = e.target.result;
                const preview = document.getElementById("image-preview");
                preview.src = uploadedImageBase64;
                preview.style.display = "block"; // Reveal the preview image
            };
            reader.readAsDataURL(file);
        }
    });

    // Attach a submit handler to the form (using the form's submit event)
    const postForm = document.querySelector(".post-options-form");
    postForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent the default form submission

        // Get values from the editable fields
        const title = document.querySelector(".editable-title").value.trim();
        const skillsToLearn = document.querySelector(".skills-to-learn").value.trim();
        const skillsToTeach = document.querySelector(".skills-to-teach").value.trim();
        const dropdownWant = document.getElementById("dropdown-want").value;
        const dropdownTeach = document.getElementById("dropdown-teach").value;

        // Basic validation: ensure required fields are filled
        if (!title || !skillsToLearn || !skillsToTeach || !dropdownWant || !dropdownTeach) {
            alert("Please fill in all required fields.");
            return;
        }

        // Build the data object to send to the backend
        const postData = {
            title: title,
            poster: sessionStorage.getItem("username"), // Static poster name
            image: uploadedImageBase64, // The Base64 image data (if any)
            skillsToLearn: skillsToLearn,
            skillsToTeach: skillsToTeach,
            desiredSkill: dropdownWant, // category
            teachSkill: dropdownTeach, // tag
            // Additional fields (e.g., timestamp) can be added here as needed
        };

        // Send the data to the backend using fetch
        fetch("/create_post", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(postData),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    alert("Post created successfully!");
                    // Optionally, store data or redirect to a success page
                    window.location.href = "/index.html";
                } else {
                    alert("Error: " + data.message);
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("Something went wrong. Please try again.");
            });
    });
});
