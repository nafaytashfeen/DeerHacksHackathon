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


// If the user clicks on any of the categories, simulate a search for a skill using that category
document.querySelectorAll(".category").forEach(category => {
    category.addEventListener("click", function() {
        const searchBar = document.querySelector("#search-bar input");
        searchBar.value = this.textContent; // Set search bar value to clicked category
        let data = getResults(); // Call the function that fetches and displays results
        displayResults(data);
    });
});


// if the user presses enter on the search bar
document.getElementById("search-bar").addEventListener("keydown", function(event){
    if (event.key === "Enter") {
        event.preventDefault(); // Prevent form submission (if inside a form)
        let data = get_results(); // get the results
        displayResults(data);
    }
});

function get_results(){
    let search_value = document.querySelector("#search-bar input").value;
    if (search_value === "" || search_value === " "){
        alert("Please enter a skill you want to learn");
    }
    let skill_set = JSON.parse(sessionStorage.getItem("skill_set"));

    const data = {
        "search": search_value,
        "skill_set": skill_set
    }

    fetch("/search_results", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            return data;
        } else {
            alert("Error: " + data.message);
        }
    })

    .catch(error => {
        console.error("Error:", error);
        alert("Something went wrong. Please try again.");
    });
}

/**
 * A function that displays the posting divs for the results
 * @param {*} results 
 */
function displayResults(results){
    const postingsSection = document.querySelector(".postings");
    postingsSection.innerHTML = ""; // Clear previous results

    results.forEach(result => {
        const postingDiv = document.createElement("div");
        postingDiv.classList.add("posting");

        postingDiv.innerHTML = `
            <div class="desired-skills">
                ${result.skills.map(skill => `<span class="skill-badge">${skill}</span>`).join("")}
            </div>
            <h3 class="posting-title">${result.title}</h3>
            <img src="data:image/png;base64,${result.image}" alt="./static/images/skills.webp" />
            <p class="description">${result.descript_teach}</p>
            <div class="footer-info">
                <p class="username">${result.postOwner}</p>
            </div>
        `;

        postingsSection.appendChild(postingDiv);
    });
}
