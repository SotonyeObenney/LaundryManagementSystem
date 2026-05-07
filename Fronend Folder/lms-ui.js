// Wait for DOM
document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");

    const serviceType = document.getElementById("serviceType");
    const shirts = document.getElementById("shirts");
    const trousers = document.getElementById("trousers");
    const traditional = document.getElementById("traditional");
    const light = document.getElementById("light");
    const heavy = document.getElementById("heavy");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        // Get values
        const data = {
            service: serviceType.value,
            shirts: parseInt(shirts.value) || 0,
            trousers: parseInt(trousers.value) || 0,
            traditional: parseInt(traditional.value) || 0,
            light: parseInt(light.value) || 0,
            heavy: parseInt(heavy.value) || 0
        };

        // 🔢 Calculate total items
        const totalItems =
            data.shirts +
            data.trousers +
            data.traditional +
            data.light +
            data.heavy;

        // ❗ Validation
        if (!data.service) {
            alert("Please select a service type");
            return;
        }

        if (totalItems === 0) {
            alert("Please add at least one item");
            return;
        }

        if (totalItems > 30) {
            alert("Maximum of 30 items exceeded");
            return;
        }

        try {
            // 🔗 Send to backend
            const response = await fetch("http://localhost:5000/orders", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                alert("Order created successfully!");

                // 🔄 Reset form
                form.reset();

                // Optional: reset numbers to 0
                shirts.value = 0;
                trousers.value = 0;
                traditional.value = 0;
                light.value = 0;
                heavy.value = 0;

                // (Optional) reload or update table
                location.reload();

            } else {
                alert(result.message || "Failed to create order");
            }

        } catch (error) {
            console.error(error);
            alert("Server error. Try again later.");
        }
    });

});