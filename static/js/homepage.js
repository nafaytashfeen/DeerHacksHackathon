document.addEventListener("DOMContentLoaded", function () {
    if (sessionStorage.getItem('signed_in') === 'true') {
        window.location.href = "/homepage.html";
    }
});