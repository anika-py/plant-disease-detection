document.addEventListener("DOMContentLoaded", function () {
    const overlay = document.querySelector(".overlay");

if (!overlay) return; // Avoid errors if the element is missing


const diagnoseLink = document.querySelector(".nav-link[href*='diagnose']");
const testPlantBtn = document.querySelector(".hero .btn");

// Function to handle the transition effect
function navigateWithTransition(event, targetUrl) {
    event.preventDefault(); // Prevent immediate navigation

    overlay.classList.add("expand"); // Expand overlay animation
    setTimeout(() => {
        window.location.href = targetUrl; // Navigate after animation
    }, 800);
    }

    // Add event listener for the Diagnose nav link
    if (diagnoseLink) {
        diagnoseLink.addEventListener("click", function (event) {
            navigateWithTransition(event, diagnoseLink.href);
        });
    }

    // Add event listener for the Test Your Plant button, but ONLY on the index page
    if (testPlantBtn && window.location.pathname === "/") { 
        testPlantBtn.addEventListener("click", function (event) {
            navigateWithTransition(event, diagnoseLink.href); // Redirect to diagnose page
        });
    }


    // ✅ Handle transition from Diagnose → Index
    const homeLink = document.querySelector(".nav-link[href*='index']");
    if (homeLink) {
        homeLink.addEventListener("click", function (event) {
            event.preventDefault();

            overlay.classList.remove("expand"); // Collapse overlay

            setTimeout(() => {
                window.location.href = homeLink.href; // Navigate after animation
            }, 800);
        });
    }

    // ✅ Ensure Diagnose Page starts with expanded overlay
    if (window.location.pathname.includes("diagnose")) {
        overlay.classList.add("expand");
    }
});
