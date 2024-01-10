async function fetchData(url) {
    const response = await fetch(url);
    const data = await response.json();
    return data;
}

async function populateDropdowns() {
    const customers = await fetchData('http://127.0.0.1:5000/api/customers');
    const countries = await fetchData('http://127.0.0.1:5000/api/countries');

    // Assuming the API responses are in the format ["Andrey", "Carl", "Jonson"]

    // Populate customer dropdown
    const customerSelect = document.getElementById("customer-select");
    customers.forEach(customer => {
        const option = document.createElement("option");
        option.value = customer;
        option.textContent = customer;
        customerSelect.appendChild(option);
    });

    // Populate country dropdown
    const countrySelect = document.getElementById("country-select");
    countries.forEach(country => {
        const option = document.createElement("option");
        option.value = country;
        option.textContent = country;
        countrySelect.appendChild(option);
    });
}

// Call the function to populate dropdowns when the page is loaded
populateDropdowns();

async function retrieve_search(customer, country) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "customer": customer,
                "country": country
            })
        });

        const responseData = await response.json();
        const tableBody = document.getElementById("table-body");
        tableBody.innerHTML = ""; // Clear previous results

        responseData.forEach(order => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${order[0]}</td>
                <td>${order[1]}</td>
                <td>${order[2]}</td>
                <td>${order[3]}</td>
                <td>${order[4]}</td>
                <td>${order[5]}</td>
                <td>${order[6]}</td>
                <td>${order[7]}</td>
                <td>${order[8]}</td>
                <td>${order[9]}</td>
                <td>${order[10]}</td>
                <td>${order[11]}</td>
                <td>${order[12]}</td>
                <td>${order[13]}</td>
            `;
            tableBody.appendChild(row);
        });

        console.log(responseData); // Handle the response from the backend
    } catch (error) {
        console.error('Error:', error);
    }
}

const form = document.getElementById("data-form");
form.addEventListener("submit", function(event) {
    event.preventDefault();

    const customerSelect = document.getElementById("customer-select");
    const countrySelect = document.getElementById("country-select");

    const selectedCustomer = customerSelect.value;
    const selectedCountry = countrySelect.value;
    console.log(selectedCountry,selectedCustomer)
    retrieve_search(selectedCustomer, selectedCountry);
});