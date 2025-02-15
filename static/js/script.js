document.addEventListener("DOMContentLoaded", function () {
    if (sessionStorage.getItem('signed_in') === 'true') {
        // User is signed in; do nothing
    } else {
        window.location.href = "/homepage.html"; // redirect to homepage if not signed in
    }
});