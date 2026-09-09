const API_URL = "http://127.0.0.1:8000";

export async function getCustomers() {
    const response = await fetch(`${API_URL}/customers`);

    if (!response.ok) {
        throw new Error("Failed to fetch customers");
    }

    return response.json();
}

export async function getStatistics() {
    const response = await fetch(`${API_URL}/statistics`);

    if (!response.ok) {
        throw new Error("Failed to fetch statistics");
    }

    return response.json();
}