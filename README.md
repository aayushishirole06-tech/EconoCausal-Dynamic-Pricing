EconoCausal -- Dynamic Pricing

Causal Machine Learning Based Pricing Recommendation System

EconoCausal Dynamic Pricing is a causal machine learning based pricing
decision-support system. It estimates the causal effect of price on
demand using Double Machine Learning (DML), evaluates multiple pricing
scenarios, and presents the results through an interactive Streamlit
dashboard.

Project Overview

The project uses the UCI Online Retail II dataset and follows this
pipeline:

UCI Online Retail II
        ↓
Data Preprocessing
        ↓
Product-Month Aggregation
        ↓
Causal Feature Engineering
        ↓
Double Machine Learning (LinearDML)
        ↓
Estimated Treatment Effects
        ↓
Dynamic Pricing Simulation
        ↓
Demand & Revenue Evaluation
        ↓
Interactive Streamlit Dashboard
        ↓
Pricing Scenario Recommendation

Objectives

Analyze historical retail transaction data.

Estimate the causal effect of price on demand.

Apply Double Machine Learning to control for observed covariates.

Simulate multiple pricing scenarios.

Compare predicted demand and revenue.

Identify the best-performing scenario among the tested price
changes.

Provide an interactive pricing decision-support dashboard.

Deploy the dashboard on Streamlit Community Cloud.

Dataset

The project uses the UCI Online Retail II dataset, containing
transactions from a UK-based online retailer from 2009--2011.

Important raw variables include:

Variable        Description

InvoiceNo     Transaction/invoice identifier
StockCode     Product identifier
Description   Product description
Quantity      Quantity purchased
InvoiceDate   Transaction date and time
UnitPrice     Unit price
CustomerID    Customer identifier
Country       Customer country
- Key business performance indicators
- Interactive price-change simulator
- Predicted demand and revenue analysis
- Pricing scenario comparison
- Revenue improvement analysis
- Demand impact analysis
- Causal Machine Learning model results
- Pricing recommendation based on tested scenario

Data Preprocessing

The raw data was cleaned by:

Removing missing CustomerID and Description records.

Removing duplicate records.

Removing cancelled transactions.

Removing non-positive quantities.

Removing non-positive unit prices.

Creating TotalPrice.

Converting date fields to datetime.

Extracting year, month, day and hour.

Combining the two yearly datasets.

Aggregating transactions into a product-month dataset.

The product-month dataset contains metrics including average price,
total quantity, total revenue, transaction count and number of
countries.

Causal Modeling

Treatment

T = AvgPrice

The treatment represents average product price.

Outcome

Y = TotalQuantity

The outcome represents demand.

Covariates

The final causal model uses:

Year
Month
PreviousQuantity
TimeIndex

PriceVsProductAvg was excluded because it is mathematically derived
from the current treatment. Current-period Transactions and
Countries were also excluded because they can be post-treatment
variables.

Double Machine Learning

The project uses LinearDML from EconML.

DML is used because the objective is not only to predict demand, but to
estimate how demand changes when price changes while accounting for
observed covariates.

Model configuration

Component                  Configuration

Causal estimator           LinearDML
Nuisance model             RandomForestRegressor
Number of trees            300
Maximum depth              10
Minimum samples per leaf   10
Cross-validation           5-fold K-Fold
Random state               42

Causal Model Result

Average Treatment Effect

ATE = -0.9257

95% confidence interval:

[-1.8075, -0.0439]

The negative treatment effect indicates that, under the assumptions of
the causal model, increasing price is estimated to reduce quantity
demanded.

The value -0.9257 is an estimated change in demand per one-unit
increase in the treatment variable. It is not a percentage
elasticity.

Dynamic Pricing Simulation

The pricing engine evaluates:

-10%, -5%, 0%, +5%, +10%, +15%, +20%

For each scenario:

Simulated Price
= Current Price × (1 + Price Change %)

Predicted Demand
= Current Demand
  + Treatment Effect × (Simulated Price - Current Price)

Predicted Revenue
= Simulated Price × Predicted Demand

Predicted demand is constrained to remain non-negative.

Pricing Scenario Results

Price Change   Predicted Demand    Predicted Revenue   Revenue Change

        -10%          8,497,054       £15,052,033.49           -8.41%
         -5%          8,491,363       £15,749,756.62           -4.17%
          0%          8,485,674       £16,434,499.97            0.00%
         +5%          8,480,164       £17,149,622.90           +4.35%
        +10%          8,474,881       £17,879,451.34           +8.79%
        +15%          8,469,729       £18,612,047.12          +13.25%
    **+20%**      **8,464,664**   **£19,340,914.28**      **+17.68%**

Key Result

The +20% price-change scenario produces the highest predicted
revenue among the tested scenarios.

Current predicted revenue: £16.43 million

+20% predicted revenue: £19.34 million

Simulated revenue improvement: +17.68%

Predicted demand change: -0.25%

Important: +20% is the best-performing scenario among the tested
price changes. It is not a guaranteed real-world revenue increase or a
globally optimal price.

Interactive Streamlit Dashboard

The project includes an interactive Streamlit dashboard.

Features

Key business performance indicators

Interactive pricing simulator

Price-change slider

Predicted demand and revenue

Pricing scenario comparison

Demand and revenue visualizations

Business impact analysis

Causal model results

Downloadable scenario results

Methodology section

Dashboard Workflow

User selects price-change scenario
              ↓
       Simulated Price
              ↓
    DML Treatment Effect
              ↓
       Predicted Demand
              ↓
       Predicted Revenue
              ↓
     Business Impact Metrics

The dashboard is a decision-support and simulation system. It does
not automatically change real-world prices.

Dashboard Sections

Key Business Results - Best tested price change - Predicted
revenue - Revenue improvement - Demand change

Interactive Pricing Simulator - User selects a price-change
scenario. - The dashboard updates predicted demand, predicted revenue
and demand change.

Scenario Analysis - Displays all tested pricing scenarios in a
comparison table. - Provides demand and revenue visualizations. - Allows
downloading scenario results.

Business Impact - Visualizes the revenue-demand trade-off.

Causal Model - Displays the DML causal results and estimated
treatment effect.

Live Dashboard

The deployed application is available here:

https://econocausal-dynamic-pricing-nrmvknll5txizjewn9bat.streamlit.app/

Run Locally

1. Clone the repository

git clone https://github.com/aayushishirole06-tech/EconoCausal-Dynamic-Pricing.git
cd EconoCausal-Dynamic-Pricing

2. Create and activate a virtual environment

Windows:

python -m venv .venv
.\.venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Run the dashboard

streamlit run app.py

If multiple Python/Streamlit installations exist:

.\.venv\Scripts\python.exe -m streamlit run app.py

Repository Structure

EconoCausal-Dynamic-Pricing/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/
│   └── processed/
│       ├── causal_modeling_data.csv
│       ├── dynamic_pricing_scenarios.csv
│       └── model_evaluation_summary.csv
│
├── notebooks/
│   ├── 04_Double_Machine_Learning.ipynb
│   ├── 05_Dynamic_Pricing_Engine.ipynb
│   └── ...
│
└── ...

Technology Stack

Category           Technology

Language           Python
Data Processing    Pandas, NumPy
Visualization      Matplotlib
Machine Learning   Scikit-learn
Causal ML          EconML
Causal Estimator   LinearDML
Nuisance Model     Random Forest
Dashboard          Streamlit
Version Control    Git & GitHub
Deployment         Streamlit Community Cloud

Project Outputs

Causal Modeling Dataset

data/processed/causal_modeling_data.csv

Contains the treatment, outcome and causal covariates used for DML.

Dynamic Pricing Scenarios

data/processed/dynamic_pricing_scenarios.csv

Contains predicted demand, predicted revenue and revenue changes for the
tested scenarios.

Model Evaluation Summary

data/processed/model_evaluation_summary.csv

Contains the main causal model evaluation results.

Limitations

Causal inference depends on assumptions about observed and
unobserved confounding.

The pricing engine evaluates predefined scenarios rather than
unrestricted numerical optimization.

The simulation uses estimated treatment effects as a local linear
approximation of demand response.

Historical observational data cannot guarantee the same response
under a future pricing intervention.

+20% is the best tested scenario, not a guaranteed globally optimal
price.

Future Scope

Product-level individualized pricing recommendations.

More granular customer and product features.

Nonlinear demand-response modeling.

Inventory-aware pricing.

Price constraints and business guardrails.

Real-time transaction integration.

Online A/B testing.

Automated causal model monitoring.

Advanced price optimization beyond predefined scenarios.

Team

EconoCausal -- Dynamic Pricing

A team project covering data preprocessing, causal machine learning,
dynamic pricing simulation, dashboard development, documentation and
deployment.

References

UCI Machine Learning Repository --- Online Retail II Dataset

EconML --- Causal Machine Learning

Double/debiased Machine Learning for Treatment and Structural
Parameters

Streamlit Documentation

License

This project is developed for academic/project evaluation purposes.