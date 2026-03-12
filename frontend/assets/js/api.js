const API_BASE = "http://localhost:8000";

async function get(endpoint) {
    const response = await fetch(API_BASE + endpoint);

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'No se pudo obtener la informacion');
    }

    return response.json();
}

async function post(endpoint, data) {
    const response = await fetch(API_BASE + endpoint, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'No se pudo completar la solicitud');
    }

    return response.json();
}