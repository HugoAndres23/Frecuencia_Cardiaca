const API_BASE = "http://localhost:8000/api/v1";

async function post(endpoint, data) {
    const response = await fetch(API_BASE + endpoint, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    return response.json();
}