document.getElementById("paymentForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const name = document.getElementById("name").value;
    const firstPaymentDay = parseInt(document.getElementById("firstPaymentDay").value);
    const secondPaymentDay = parseInt(document.getElementById("secondPaymentDay").value);
    const amount = parseFloat(document.getElementById("amount").value);

    // Perform validation checks
    if (name === "" || isNaN(firstPaymentDay) || isNaN(secondPaymentDay) || isNaN(amount) ||
        firstPaymentDay < 1 || firstPaymentDay > 31 || secondPaymentDay < 1 || secondPaymentDay > 31) {
        // Display error message or highlight invalid fields
        alert("Please fill out all fields with valid values. Days must be between 1 and 31.");
        return;
    }

    // Get form data
    const formData = new FormData(event.target);
    const paymentData = {
        name: formData.get("name"),
        firstPaymentDay: firstPaymentDay,
        secondPaymentDay: secondPaymentDay,
        amount: amount
    };

    // Send API request
    fetch("http://127.0.0.1:5000/api/payment", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(paymentData)
    })
    .then(response => response.json())
    .then(data => {
        console.log("API Response:", data);
        // Handle API response as needed
    })
    .catch(error => {
        console.error("Error:", error);
        // Handle errors
    });
});
