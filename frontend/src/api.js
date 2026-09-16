const API_URL = "http://127.0.0.1:8000";

export async function getHealth() {
    const response = await fetch(`${API_URL}/health`);

    if (!response.ok) {
        throw new Error(`Health API error: ${response.status}`);
    }

    return response.json();
}

export async function getCustomers() {
    const response = await fetch(`${API_URL}/customers`);

    if (!response.ok) {
        throw new Error(`Customers API error: ${response.status}`);
    }

    const data = await response.json();

    return data.customers || [];
}

export async function getStatistics() {
    const response = await fetch(`${API_URL}/statistics`);

    if (!response.ok) {
        throw new Error(`Statistics API error: ${response.status}`);
    }

    return response.json();
}