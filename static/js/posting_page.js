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

document.addEventListener("DOMContentLoaded", async function () {
    // Get post ID from URL
    const urlParams = new URLSearchParams(window.location.search);
    const postId = urlParams.get("id");

    if (!postId) {
        document.body.innerHTML = "<h2>Post not found</h2>";
        return;
    }

    try {
        // Fetch post data from Flask backend
        const response = await fetch(`/get_post/${postId}`);
        if (!response.ok) {
            throw new Error("Post not found");
        }

        const post = await response.json();

        // Populate the page with post data
        document.querySelector(".post-title").textContent = post.title;
        document.querySelector(".post-date").textContent = `Posted: ${post.current_date}`;
        document.querySelector(".poster-name").innerHTML = `<strong>Posted By:</strong> ${post.postOwner}`;

        // Handle image display
        if (post.image) {
            document.querySelector(".post-image").src = post.image;
            document.querySelector(".post-image").style.display = "block";
        } else {
            document.querySelector(".post-image").style.display = "none";
        }

        document.querySelector(".post-description").textContent = post.descript_learn;

    } catch (error) {
        document.body.innerHTML = `<h2>${error.message}</h2>`;
    }
});
