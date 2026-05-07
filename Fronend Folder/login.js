// Wait for the page to fully load
document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");

    form.addEventListener("submit", async function (e) {
        e.preventDefault(); // stop page refresh

        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();

        // 🔒 Basic validation
        if (email === "" || password === "") {
            alert("Please fill in all fields");
            return;
        }

        try {
            // 🔗 Send data to backend (Python API)
            const response = await fetch("http://localhost:5000/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (response.ok) {
                alert("Login successful!");

                // Example: redirect after login
                window.location.href = "dashboard.html";

            } else {
                alert(data.message || "Login failed");
            }

        } catch (error) {
            console.error("Error:", error);
            alert("Server error. Please try again later.");
        }
    });

});