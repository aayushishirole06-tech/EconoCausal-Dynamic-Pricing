import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="EconoCausal Dynamic Pricing",
    page_icon="💰",
    layout="wide"
)


# =========================================================
# CUSTOM STYLING
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    opacity: 0.75;
    margin-bottom: 25px;
}

.recommendation {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid rgba(128,128,128,0.3);
    margin-top: 15px;
    margin-bottom: 25px;
}

.section-title {
    font-size: 28px;
    font-weight: 650;
    margin-top: 20px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

scenario_df = pd.read_csv(
    "data/processed/dynamic_pricing_scenarios.csv"
)

evaluation_df = pd.read_csv(
    "data/processed/model_evaluation_summary.csv"
)


# =========================================================
# BASIC VALUES
# =========================================================

best_row = scenario_df.loc[
    scenario_df["PredictedRevenue"].idxmax()
]

current_row = scenario_df[
    scenario_df["PriceChangePct"] == 0
].iloc[0]

best_price = best_row["PriceChangePct"]
best_revenue = best_row["PredictedRevenue"]
best_demand = best_row["PredictedDemand"]

current_revenue = current_row["PredictedRevenue"]
current_demand = current_row["PredictedDemand"]

revenue_improvement = (
    (best_revenue - current_revenue)
    / current_revenue
) * 100

demand_change = (
    (best_demand - current_demand)
    / current_demand
) * 100


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">💰 EconoCausal Dynamic Pricing</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Causal Machine Learning Based Pricing Recommendation System'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "This dashboard uses Double Machine Learning (DML) "
    "to estimate the causal effect of price on demand "
    "and evaluate different pricing scenarios."
)


# =========================================================
# TOP KPI CARDS
# =========================================================

st.markdown(
    '<div class="section-title">📌 Key Business Results</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Best Tested Price Change",
    f"+{best_price:.0f}%"
)

col2.metric(
    "Predicted Revenue",
    f"£{best_revenue:,.0f}"
)

col3.metric(
    "Revenue Improvement",
    f"+{revenue_improvement:.2f}%"
)

col4.metric(
    "Demand Change",
    f"{demand_change:.2f}%"
)


# =========================================================
# INTERACTIVE SCENARIO SELECTOR
# =========================================================

st.markdown(
    '<div class="section-title">🎛️ Interactive Pricing Simulator</div>',
    unsafe_allow_html=True
)

available_prices = sorted(
    scenario_df["PriceChangePct"].unique()
)

selected_price = st.select_slider(
    "Select a price-change scenario",
    options=available_prices,
    value=best_price,
    format_func=lambda x: f"{x:+.0f}%"
)


selected_row = scenario_df[
    scenario_df["PriceChangePct"] == selected_price
].iloc[0]

selected_demand = selected_row["PredictedDemand"]
selected_revenue = selected_row["PredictedRevenue"]
selected_revenue_change = selected_row["RevenueChangePct"]

selected_demand_change = (
    (selected_demand - current_demand)
    / current_demand
) * 100


# =========================================================
# SELECTED SCENARIO KPIs
# =========================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Selected Price Change",
    f"{selected_price:+.0f}%"
)

col2.metric(
    "Predicted Demand",
    f"{selected_demand:,.0f}"
)

col3.metric(
    "Predicted Revenue",
    f"£{selected_revenue:,.0f}",
    f"{selected_revenue_change:+.2f}%"
)

col4.metric(
    "Demand Change",
    f"{selected_demand_change:+.2f}%"
)

st.caption(
    f"Revenue impact relative to current pricing: "
    f"{selected_revenue_change:+.2f}%"
)
st.caption(
    f"Demand impact relative to current pricing: "
    f"{selected_demand_change:+.2f}%"
)


# =========================================================
# RECOMMENDATION
# =========================================================

st.markdown(
    '<div class="section-title">🎯 Pricing Recommendation</div>',
    unsafe_allow_html=True
)

if selected_price == best_price:

    st.success(
        f"**Best Tested Scenario:** A {selected_price:+.0f}% "
        f"price change produces the highest predicted revenue "
        f"of **£{selected_revenue:,.2f}**, representing a "
        f"**{selected_revenue_change:.2f}% revenue improvement** "
        f"over the current scenario."
    )

else:

    st.info(
        f"The selected {selected_price:+.0f}% price scenario "
        f"produces predicted revenue of "
        f"**£{selected_revenue:,.2f}**."
    )


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3 = st.tabs([
    "📊 Scenario Analysis",
    "📈 Business Impact",
    "🔬 Causal Model"
])


# =========================================================
# TAB 1 — SCENARIO ANALYSIS
# =========================================================

with tab1:

    st.subheader("Pricing Scenario Comparison")

    display_df = scenario_df.copy()

    display_df["Price Change (%)"] = display_df[
        "PriceChangePct"
    ].map(lambda x: f"{x:+.0f}%")

    display_df["Predicted Demand"] = display_df[
        "PredictedDemand"
    ].map(lambda x: f"{x:,.0f}")

    display_df["Predicted Revenue (£)"] = display_df[
        "PredictedRevenue"
    ].map(lambda x: f"£{x:,.2f}")

    display_df["Revenue Change (%)"] = display_df[
        "RevenueChangePct"
    ].map(lambda x: f"{x:+.2f}%")

    display_df = display_df[
        [
            "Price Change (%)",
            "Predicted Demand",
            "Predicted Revenue (£)",
            "Revenue Change (%)"
        ]
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    csv_data = scenario_df.to_csv(index=False)

    st.download_button(
        label="⬇️ Download Scenario Results",
        data=csv_data,
        file_name="dynamic_pricing_scenarios.csv",
        mime="text/csv"
    )


# =========================================================
# TAB 2 — BUSINESS IMPACT
# =========================================================

with tab2:

    st.subheader("Revenue vs Price Change")

    fig1, ax1 = plt.subplots(figsize=(9, 5))

    ax1.plot(
        scenario_df["PriceChangePct"],
        scenario_df["PredictedRevenue"],
        marker="o",
        linewidth=2
    )

    ax1.axhline(
    current_revenue,
    linestyle="--",
    linewidth=2,
    label="Current Revenue"
)

    ax1.set_xlabel("Price Change (%)")
    ax1.set_ylabel("Predicted Revenue (£)")
    ax1.set_title("Predicted Revenue vs Price Change")
    ax1.grid(True)
    ax1.legend()

    st.pyplot(fig1)

    st.subheader("Demand vs Price Change")

    fig2, ax2 = plt.subplots(figsize=(9, 5))

    ax2.plot(
        scenario_df["PriceChangePct"],
        scenario_df["PredictedDemand"],
        marker="o",
        linewidth=2
    )

    ax2.axhline(
        current_demand,
        linestyle="--",
        linewidth=2,
        label="Current Demand"
    )

    ax2.set_xlabel("Price Change (%)")
    ax2.set_ylabel("Predicted Demand (Units)")
    ax2.set_title("Predicted Demand vs Price Change")
    ax2.legend()
    ax2.grid(True)

st.pyplot(fig2)

st.subheader("Current vs Selected Scenario")

comparison = pd.DataFrame({
        "Metric": [
            "Price Change",
            "Demand",
            "Revenue"
        ],
        "Current": [
            "0%",
            f"{current_demand:,.0f}",
            f"£{current_revenue:,.2f}"
        ],
        "Selected Scenario": [
            f"{selected_price:+.0f}%",
            f"{selected_demand:,.0f}",
            f"£{selected_revenue:,.2f}"
        ]
    })

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Price Change (%)": st.column_config.TextColumn(
            "Price Change"
        ),
        "Predicted Demand": st.column_config.NumberColumn(
            "Predicted Demand",
            format="%d"
        ),
        "Predicted Revenue (£)": st.column_config.NumberColumn(
            "Predicted Revenue",
            format="£%.2f"
        ),
        "Revenue Change (%)": st.column_config.NumberColumn(
            "Revenue Change"
        )
    }
)


# =========================================================
# TAB 3 — CAUSAL MODEL
# =========================================================

with tab3:

    st.subheader("Double Machine Learning Results")

    ate = evaluation_df.loc[
        evaluation_df["Metric"] == "ATE",
        "Value"
    ].iloc[0]

    ci_lower = evaluation_df.loc[
        evaluation_df["Metric"] == "ATE 95% CI Lower",
        "Value"
    ].iloc[0]

    ci_upper = evaluation_df.loc[
        evaluation_df["Metric"] == "ATE 95% CI Upper",
        "Value"
    ].iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Treatment Effect",
        f"{ate:.4f}"
    )

    col2.metric(
        "95% CI Lower",
        f"{ci_lower:.4f}"
    )

    col3.metric(
        "95% CI Upper",
        f"{ci_upper:.4f}"
    )

    st.info(
        "The negative ATE indicates that increasing price "
        "has an estimated negative causal effect on demand "
        "under the DML model assumptions."
    )

    st.subheader("Interpretation")

    st.write(
        f"The estimated Average Treatment Effect is "
        f"**{ate:.4f}**. The 95% confidence interval ranges "
        f"from **{ci_lower:.4f}** to **{ci_upper:.4f}**, "
        "which remains below zero."
    )


# =========================================================
# METHODOLOGY
# =========================================================

st.header("📚 Methodology")

with st.expander("How the pricing recommendation is generated"):

    st.markdown("""
    **1. Historical Retail Data**

    Transaction-level retail data is aggregated into a
    product-month panel containing price, demand and
    historical demand information.

    **2. Causal Modeling**

    Double Machine Learning (DML) is used to estimate the
    causal effect of price on demand while controlling for
    relevant observed covariates.

    **3. Treatment Effect**

    The estimated treatment effect represents the expected
    change in demand associated with a one-unit change in price,
    under the model assumptions.

    **4. Price Simulation**

    Multiple price-change scenarios are evaluated from
    -10% to +20%.

    **5. Revenue Evaluation**

    For each scenario, predicted demand and revenue are
    calculated and compared with the current pricing scenario.

    **6. Recommendation**

    The scenario with the highest predicted revenue among
    the tested price changes is presented as the
    **best tested pricing scenario**.
    """)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "EconoCausal-Dynamic-Pricing | "
    "Double Machine Learning + Dynamic Pricing Simulation"
)