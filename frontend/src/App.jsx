import React, { useEffect, useState } from "react";
import { getCustomers, getStatistics } from "./api";

function App() {
    const [customers, setCustomers] = useState([]);
    const [statistics, setStatistics] = useState(null);
    const [error, setError] = useState("");

    useEffect(() => {
        async function loadData() {
            try {
                const customerData = await getCustomers();
                const statisticsData = await getStatistics();

                setCustomers(customerData);
                setStatistics(statisticsData);
            } catch (err) {
                setError(err.message);
            }
        }

        loadData();
    }, []);

    return (
        <div style={{ padding: "30px", fontFamily: "Arial" }}>
            <h1>EconoCausal Dynamic Pricing</h1>

            <h2>FastAPI Connection</h2>

            {error && (
                <p style={{ color: "red" }}>
                    Error: {error}
                </p>
            )}

            {statistics && (
                <div>
                    <h3>Statistics</h3>
                    <pre>
                        {JSON.stringify(statistics, null, 2)}
                    </pre>
                </div>
            )}

            <h2>Customers</h2>

            <p>Total Customers: {customers.length}</p>

            <table border="1" cellPadding="10">
                <thead>
                    <tr>
                        <th>Customer ID</th>
                        <th>Response</th>
                        <th>Discount</th>
                        <th>Recommended Price</th>
                    </tr>
                </thead>

                <tbody>
                    {customers.slice(0, 20).map((customer, index) => (
                        <tr key={index}>
                            <td>
                                {customer.CustomerID}
                            </td>

                            <td>
                                {customer.CustomerResponse}
                            </td>

                            <td>
                                {customer.RecommendedDiscount}
                            </td>

                            <td>
                                {customer.RecommendedPrice}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default App;