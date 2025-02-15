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
        fetch("http://127.0.0.1:5001/create_post", {
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
                    window.location.href = "/post_success.html"; // Example redirect
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
