import React, { useEffect, useState } from "react";
import {
    getHealth,
    getCustomers,
    getStatistics
} from "./api";

function App() {
    const [health, setHealth] = useState(null);
    const [customers, setCustomers] = useState([]);
    const [statistics, setStatistics] = useState({});
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function loadData() {
            try {
                setLoading(true);
                setError("");

                const healthData = await getHealth();
                const customerData = await getCustomers();
                const statisticsData = await getStatistics();

                setHealth(healthData);
                setCustomers(customerData);
                setStatistics(statisticsData);
            } catch (err) {
                console.error(err);
                setError(err.message || "Failed to fetch data");
            } finally {
                setLoading(false);
            }
        }

        loadData();
    }, []);

    return (
        <div style={styles.page}>

            <div style={styles.header}>
                <h1 style={styles.title}>
                    EconoCausal Dynamic Pricing
                </h1>

                <p style={styles.subtitle}>
                    Causal Machine Learning Based Dynamic Pricing System
                </p>
            </div>

            <div style={styles.connectionCard}>
                <h2>FastAPI Connection</h2>

                {loading && (
                    <p style={styles.blue}>
                        Connecting to FastAPI...
                    </p>
                )}

                {!loading && !error && health && (
                    <p style={styles.green}>
                        Connected Successfully
                    </p>
                )}

                {error && (
                    <p style={styles.red}>
                        Error: {error}
                    </p>
                )}
            </div>

            <div style={styles.cards}>

                <div style={styles.card}>
                    <h3>Total Customers</h3>
                    <p style={styles.number}>
                        {statistics.total_customers !== undefined
                            ? statistics.total_customers
                            : customers.length}
                    </p>
                </div>

                <div style={styles.card}>
                    <h3>Average Treatment Effect</h3>
                    <p style={styles.number}>
                        {statistics.average_treatment_effect !== undefined
                            ? Number(
                                statistics.average_treatment_effect
                            ).toFixed(3)
                            : "N/A"}
                    </p>
                </div>

                <div style={styles.card}>
                    <h3>Average Discount</h3>
                    <p style={styles.number}>
                        {statistics.average_recommended_discount !== undefined
                            ? Number(
                                statistics.average_recommended_discount
                            ).toFixed(2)
                            : "N/A"}
                    </p>
                </div>

                <div style={styles.card}>
                    <h3>Average Recommended Price</h3>
                    <p style={styles.number}>
                        {statistics.average_recommended_price !== undefined
                            ? Number(
                                statistics.average_recommended_price
                            ).toFixed(2)
                            : "N/A"}
                    </p>
                </div>

            </div>

            <div style={styles.summaryCard}>
                <h2>System Summary</h2>

                <div style={styles.summaryGrid}>

                    <div>
                        <strong>API Status:</strong>
                        <span style={styles.greenText}>
                            {health?.status || "Unknown"}
                        </span>
                    </div>

                    <div>
                        <strong>Dataset Loaded:</strong>
                        <span style={styles.greenText}>
                            {health?.dataset_loaded ? "Yes" : "No"}
                        </span>
                    </div>

                    <div>
                        <strong>Customers Available:</strong>
                        <span>
                            {health?.customers || customers.length}
                        </span>
                    </div>

                </div>
            </div>

            <div style={styles.tableCard}>

                <div style={styles.tableHeader}>
                    <h2>Customer Pricing Recommendations</h2>

                    <span style={styles.countBadge}>
                        {customers.length} Customers
                    </span>
                </div>

                {loading && (
                    <p>Loading customer data...</p>
                )}

                {!loading && error && (
                    <p style={styles.red}>
                        Unable to load customer data.
                    </p>
                )}

                {!loading &&
                    !error &&
                    customers.length === 0 && (
                        <p>No customer data available.</p>
                    )}

                {customers.length > 0 && (
                    <div style={styles.tableContainer}>

                        <table style={styles.table}>

                            <thead>
                                <tr>
                                    <th style={styles.th}>
                                        Customer ID
                                    </th>

                                    <th style={styles.th}>
                                        Total Spend
                                    </th>

                                    <th style={styles.th}>
                                        Total Quantity
                                    </th>

                                    <th style={styles.th}>
                                        Response
                                    </th>

                                    <th style={styles.th}>
                                        Discount
                                    </th>

                                    <th style={styles.th}>
                                        Recommended Price
                                    </th>

                                    <th style={styles.th}>
                                        Pricing Strategy
                                    </th>

                                    <th style={styles.th}>
                                        Treatment Effect
                                    </th>
                                </tr>
                            </thead>

                            <tbody>
                                {customers
                                    .slice(0, 100)
                                    .map((customer, index) => (
                                        <tr
                                            key={
                                                customer.CustomerID ||
                                                index
                                            }
                                        >

                                            <td style={styles.td}>
                                                {
                                                    customer.CustomerID
                                                }
                                            </td>

                                            <td style={styles.td}>
                                                {customer.TotalSpend !==
                                                undefined
                                                    ? Number(
                                                        customer.TotalSpend
                                                    ).toFixed(2)
                                                    : "N/A"}
                                            </td>

                                            <td style={styles.td}>
                                                {
                                                    customer.TotalQuantity ??
                                                    "N/A"
                                                }
                                            </td>

                                            <td style={styles.td}>
                                                {
                                                    customer.CustomerResponse ||
                                                    "N/A"
                                                }
                                            </td>

                                            <td style={styles.td}>
                                                {customer.RecommendedDiscount !==
                                                undefined
                                                    ? Number(
                                                        customer.RecommendedDiscount
                                                    ).toFixed(2)
                                                    : "N/A"}
                                            </td>

                                            <td style={styles.td}>
                                                {customer.RecommendedPrice !==
                                                undefined
                                                    ? Number(
                                                        customer.RecommendedPrice
                                                    ).toFixed(2)
                                                    : "N/A"}
                                            </td>

                                            <td style={styles.td}>
                                                {
                                                    customer.PricingStrategy ||
                                                    "N/A"
                                                }
                                            </td>

                                            <td style={styles.td}>
                                                {customer.IndividualTreatmentEffect !==
                                                undefined
                                                    ? Number(
                                                        customer.IndividualTreatmentEffect
                                                    ).toFixed(3)
                                                    : customer.AverageTreatmentEffect !==
                                                        undefined
                                                    ? Number(
                                                        customer.AverageTreatmentEffect
                                                    ).toFixed(3)
                                                    : "N/A"}
                                            </td>

                                        </tr>
                                    ))}
                            </tbody>

                        </table>
                    </div>
                )}

                {customers.length > 100 && (
                    <p style={styles.note}>
                        Showing first 100 customers out of{" "}
                        {customers.length}.
                    </p>
                )}

            </div>

            <div style={styles.footer}>
                <p>
                    EconoCausal | Dynamic Pricing using Causal Machine Learning
                </p>
            </div>

        </div>
    );
}

const styles = {
    page: {
        fontFamily: "Arial, sans-serif",
        backgroundColor: "#f4f6f8",
        minHeight: "100vh",
        padding: "30px"
    },

    header: {
        backgroundColor: "#ffffff",
        padding: "25px",
        borderRadius: "12px",
        marginBottom: "20px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)"
    },

    title: {
        margin: "0 0 10px 0",
        fontSize: "36px",
        color: "#222222"
    },

    subtitle: {
        margin: 0,
        fontSize: "18px",
        color: "#666666"
    },

    connectionCard: {
        backgroundColor: "#ffffff",
        padding: "20px",
        borderRadius: "12px",
        marginBottom: "20px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)"
    },

    cards: {
        display: "grid",
        gridTemplateColumns: "repeat(4, minmax(200px, 1fr))",
        gap: "20px",
        marginBottom: "20px"
    },

    card: {
        backgroundColor: "#ffffff",
        padding: "22px",
        borderRadius: "12px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)"
    },

    number: {
        fontSize: "30px",
        fontWeight: "bold",
        margin: "15px 0 0 0",
        color: "#222222"
    },

    summaryCard: {
        backgroundColor: "#ffffff",
        padding: "22px",
        borderRadius: "12px",
        marginBottom: "20px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)"
    },

    summaryGrid: {
        display: "grid",
        gridTemplateColumns: "repeat(3, 1fr)",
        gap: "20px",
        marginTop: "15px"
    },

    greenText: {
        color: "green",
        fontWeight: "bold",
        marginLeft: "8px"
    },

    connectionText: {
        color: "#333333"
    },

    tableCard: {
        backgroundColor: "#ffffff",
        padding: "22px",
        borderRadius: "12px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)"
    },

    tableHeader: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: "20px"
    },

    countBadge: {
        backgroundColor: "#eeeeee",
        padding: "8px 12px",
        borderRadius: "20px",
        fontWeight: "bold"
    },

    tableContainer: {
        width: "100%",
        overflowX: "auto"
    },

    table: {
        width: "100%",
        borderCollapse: "collapse",
        minWidth: "1000px"
    },

    th: {
        border: "1px solid #cccccc",
        padding: "12px",
        backgroundColor: "#eeeeee",
        textAlign: "left",
        whiteSpace: "nowrap"
    },

    td: {
        border: "1px solid #cccccc",
        padding: "12px",
        whiteSpace: "nowrap"
    },

    green: {
        color: "green",
        fontWeight: "bold",
        fontSize: "18px"
    },

    red: {
        color: "red",
        fontWeight: "bold"
    },

    blue: {
        color: "blue",
        fontWeight: "bold"
    },

    note: {
        marginTop: "15px",
        color: "#666666"
    },

    footer: {
        textAlign: "center",
        marginTop: "25px",
        color: "#777777"
    }
};

export default App;
