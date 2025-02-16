document.addEventListener("DOMContentLoaded", function () {
    if (sessionStorage.getItem('signed_in') === 'true') {
        // User is signed in; do nothing
    } else {
        window.location.href = "/homepage.html"; // redirect to homepage if not signed in
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

document.addEventListener("DOMContentLoaded", function () {
    fetch("/get_postings")
        .then(response => response.json())
        .then(data => {
            const postingsContainer = document.getElementsByClassName("postings")[0]; // Ensure this div exists in your HTML
            // postingsContainer.innerHTML = "";

            data.forEach(post => {
                const postElement = document.createElement("div");
                postElement.classList.add("posting"); 
                postElement.setAttribute('data-post-id', post.postId);
            
                postElement.innerHTML = `
                    <div class="desired-skills">
                        <span class="skill-badge">${post.skills_wanted}</span>
                    </div>
                    <h3 class="posting-title">${post.title}</h3>
                    <img src="${post.image || './static/images/skills.webp'}" alt="" />
                    <p class="description">${post.descript_learn}</p>
                    <div class="footer-info">
                        <p class="username">${post.postOwner}</p>
                    </div>
                `;
            
                // Attach click listener immediately after creating the element
                postElement.addEventListener("click", function () {
                    const postId = this.getAttribute("data-post-id");
                    window.location.href = `posting_page.html?id=${postId}`;
                });
            
                postingsContainer.appendChild(postElement);
            });
            
        })
        .catch(error => console.error("Error fetching postings:", error));
});

  

// If the user clicks on any of the categories, simulate a search for a skill using that category
document.querySelectorAll(".category").forEach(category => {
    category.addEventListener("click", function () {
        const searchBar = document.querySelector("#search-bar input");
        searchBar.value = this.textContent; // Set search bar value to clicked category
        let data = getResults(); // Call the function that fetches and displays results
        displayResults(data);
    });
});


// if the user presses enter on the search bar
document.getElementById("search-bar").addEventListener("keydown", async function (event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Prevent form submission (if inside a form)
        let data = await get_results(); // get the results
        console.log("this is an array:" + data)
        displayResults(data);
    }
});

async function get_results() {
    let search_value = document.querySelector("#search-bar input").value;
    if (search_value === "" || search_value === " ") {
        alert("Please enter a skill you want to learn");
        return; // Prevent further execution if the search value is empty
    }

    let skill_set = JSON.parse(sessionStorage.getItem("skill_set"));

    const search_data = {
        "search": search_value,
        "skill_set": skill_set
    };

    try {
        const response = await fetch("/search_results", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(search_data)
        });

        const data = await response.json();
        console.log(data.success)
        if (data.success) {
            console.log(data["data"])
            return data["data"]; // Return the actual data to be used later
        } else {
            alert("Error: " + data.message);
            return []; // Return empty array in case of error
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong. Please try again.");
        return []; // Return empty array in case of error
    }
}


/**
 * A function that displays the posting divs for the results
 * @param {*} results 
 */
function displayResults(results) {
    const postingsSection = document.querySelector(".postings");
    postingsSection.innerHTML = ""; // Clear previous results

    if (Array.isArray(results)) {
        console.log("hi + " + results)

        results.forEach(result => {
            const postElement = document.createElement("div");
            postElement.classList.add("posting"); // Assign class directly

            postElement.setAttribute('data-post-id', result.postId);

            postElement.innerHTML = `
                <!-- Skills at the top -->
                <div class="desired-skills">
                <span class="skill-badge">${result.skills_wanted}</span>
                    
                </div>

                <!-- Posting Title -->
                <h3 class="posting-title">${result.title}</h3>

                <!-- Large Picture -->
                <img src="${result.image || './static/images/skills.webp'}" alt="" />

                <!-- Description -->
                <p class="description">
                    ${result.descript_learn}
                </p>

                <!-- Username at the bottom -->
                <div class="footer-info">
                    <p class="username">${result.postOwner}</p>
                </div>
            `;

                        
            // Attach click listener immediately after creating the element
            postElement.addEventListener("click", function () {
                const postId = this.getAttribute("data-post-id");
                window.location.href = `posting_page.html?id=${postId}`;
            });

            postingsSection.appendChild(postElement);
        });

    }
}