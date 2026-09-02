from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# 1. FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="EconoCausal Dynamic Pricing API",
    description="Customer-level causal dynamic pricing API",
    version="1.0.0"
)


# ============================================================
# 2. CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# 3. PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "dynamic_pricing_recommendations.csv"
)


# ============================================================
# 4. LOAD DATASET
# ============================================================

def load_dataset():

    if not DATA_FILE.exists():

        print("")
        print("ERROR: Dataset not found.")
        print(f"Expected file:")
        print(DATA_FILE)
        print("")

        return pd.DataFrame()

    try:

        data = pd.read_csv(DATA_FILE)

        if data.empty:

            print("WARNING: Dataset is empty.")

            return pd.DataFrame()

        return data

    except Exception as error:

        print(
            f"ERROR while loading dataset: {error}"
        )

        return pd.DataFrame()


df = load_dataset()


# ============================================================
# 5. CLEAN DATA
# ============================================================

if not df.empty:

    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    df = df.drop_duplicates()

    df = df.reset_index(drop=True)


# ============================================================
# 6. JSON VALUE CONVERSION
# ============================================================

def convert_value(value):

    if pd.isna(value):

        return None

    if isinstance(
        value,
        (
            np.integer,
            np.int64,
            np.int32
        )
    ):

        return int(value)

    if isinstance(
        value,
        (
            np.floating,
            np.float64,
            np.float32
        )
    ):

        return float(value)

    return value


# ============================================================
# 7. ROW TO JSON
# ============================================================

def row_to_dict(row):

    result = {}

    for column in row.index:

        result[column] = convert_value(
            row[column]
        )

    return result


# ============================================================
# 8. ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "project": "EconoCausal",
        "application": "Dynamic Pricing System",
        "status": "running",
        "version": "1.0.0"
    }


# ============================================================
# 9. HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    if df.empty:

        return {
            "status": "warning",
            "dataset_loaded": False,
            "message": "Pricing dataset is not loaded."
        }

    customer_count = 0

    if "CustomerID" in df.columns:

        customer_count = int(
            df["CustomerID"].nunique()
        )

    else:

        customer_count = len(df)

    return {
        "status": "healthy",
        "dataset_loaded": True,
        "customers": customer_count
    }


# ============================================================
# 10. DATASET INFORMATION
# ============================================================

@app.get("/dataset-info")
def dataset_info():

    if df.empty:

        raise HTTPException(
            status_code=500,
            detail="Dataset is not loaded."
        )

    if "CustomerID" in df.columns:

        customer_count = int(
            df["CustomerID"].nunique()
        )

    else:

        customer_count = len(df)

    return {
        "rows": int(len(df)),
        "columns": list(df.columns),
        "customers": customer_count,
        "file": str(DATA_FILE)
    }


# ============================================================
# 11. GET ALL CUSTOMERS
# ============================================================

@app.get("/customers")
def get_customers():

    if df.empty:

        raise HTTPException(
            status_code=500,
            detail="Dataset is not loaded."
        )

    records = []

    for _, row in df.iterrows():

        records.append(
            row_to_dict(row)
        )

    return {
        "count": len(records),
        "customers": records
    }


# ============================================================
# 12. GET CUSTOMER
# ============================================================

@app.get("/customer/{customer_id}")
def get_customer(customer_id: str):

    if df.empty:

        raise HTTPException(
            status_code=500,
            detail="Dataset is not loaded."
        )

    if "CustomerID" not in df.columns:

        raise HTTPException(
            status_code=500,
            detail="CustomerID column is missing."
        )

    customer = df[
        df["CustomerID"].astype(str)
        == str(customer_id)
    ]

    if customer.empty:

        raise HTTPException(
            status_code=404,
            detail=(
                f"Customer {customer_id} "
                "was not found."
            )
        )

    row = customer.iloc[0]

    return row_to_dict(row)


# ============================================================
# 13. CUSTOMER PRICING RECOMMENDATION
# ============================================================

@app.get("/customer/{customer_id}/pricing")
def customer_pricing(customer_id: str):

    if df.empty:

        raise HTTPException(
            status_code=500,
            detail="Dataset is not loaded."
        )

    if "CustomerID" not in df.columns:

        raise HTTPException(
            status_code=500,
            detail="CustomerID column is missing."
        )

    customer = df[
        df["CustomerID"].astype(str)
        == str(customer_id)
    ]

    if customer.empty:

        raise HTTPException(
            status_code=404,
            detail=(
                f"Customer {customer_id} "
                "was not found."
            )
        )

    row = customer.iloc[0]

    # --------------------------------------------------------
    # Helper for flexible column names
    # --------------------------------------------------------

    def get_column(
        column_names,
        default=None
    ):

        for column in column_names:

            if column in row.index:

                return convert_value(
                    row[column]
                )

        return default

    return {

        "CustomerID": get_column(
            ["CustomerID"]
        ),

        "TreatmentEffect": get_column(
            [
                "IndividualTreatmentEffect",
                "TreatmentEffect"
            ]
        ),

        "CustomerResponse": get_column(
            [
                "CustomerResponse"
            ]
        ),

        "RecommendedDiscount": get_column(
            [
                "RecommendedDiscount",
                "OptimalDiscount"
            ]
        ),

        "PricingStrategy": get_column(
            [
                "PricingStrategy",
                "OptimizationStrategy"
            ]
        ),

        "CurrentPrice": get_column(
            [
                "CurrentAveragePrice",
                "AverageUnitPrice"
            ]
        ),

        "RecommendedPrice": get_column(
            [
                "RecommendedPrice",
                "OptimalPrice"
            ]
        ),

        "ExpectedRevenue": get_column(
            [
                "ExpectedRevenue",
                "AdjustedExpectedRevenue",
                "RecommendedRevenue"
            ]
        ),

        "PreviousSpend": get_column(
            [
                "PreviousSpend"
            ]
        ),

        "PreviousTransactions": get_column(
            [
                "PreviousTransactions"
            ]
        ),

        "RecencyDays": get_column(
            [
                "RecencyDays"
            ]
        )
    }


# ============================================================
# 14. HIGH RESPONSE CUSTOMERS
# ============================================================

@app.get("/customers/high-response")
def high_response_customers():

    if df.empty:

        raise HTTPException(
            status_code=500,
            detail="Dataset is not loaded."
        )

    if "IndividualTreatmentEffect" not in df.columns:

        raise HTTPException(
            status_code=500,
            detail=(
                "IndividualTreatmentEffect "
                "column is missing."
            )
        )

    result = df[
        df["IndividualTreatmentEffect"] > 0
    ].copy()

    result = result.sort_values(
        "IndividualTreatmentEffect",
        ascending=False
    )

    records = []

    for _, row in result.iterrows():

        records.append(
            row_to_dict(row)
        )

    return {
        "count": len(records),
        "customers": records
    }


# ============================================================
# 15. PRICING STRATEGY SUMMARY
# ============================================================

@app.get("/pricing-summary")
def pricing_summary():

    if df.empty:

        raise HTTPException(
            status_code=500,
            detail="Dataset is not loaded."
        )

    if "PricingStrategy" not in df.columns:

        raise HTTPException(
            status_code=500,
            detail="PricingStrategy column is missing."
        )

    if "CustomerID" in df.columns:

        summary = (
            df.groupby("PricingStrategy")
            .agg(
                Customers=(
                    "CustomerID",
                    "nunique"
                )
            )
            .reset_index()
        )

    else:

        summary = (
            df["PricingStrategy"]
            .value_counts()
            .reset_index()
        )

        summary.columns = [
            "PricingStrategy",
            "Customers"
        ]

    records = []

    for _, row in summary.iterrows():

        records.append(
            row_to_dict(row)
        )

    return {
        "strategies": records
    }


# ============================================================
# 16. STATISTICS
# ============================================================

@app.get("/statistics")
def statistics():

    if df.empty:

        raise HTTPException(
            status_code=500,
            detail="Dataset is not loaded."
        )

    result = {}

    # --------------------------------------------------------
    # Customer count
    # --------------------------------------------------------

    if "CustomerID" in df.columns:

        result["total_customers"] = int(
            df["CustomerID"].nunique()
        )

    else:

        result["total_customers"] = int(
            len(df)
        )

    # --------------------------------------------------------
    # Treatment effect
    # --------------------------------------------------------

    if "IndividualTreatmentEffect" in df.columns:

        result[
            "average_treatment_effect"
        ] = float(
            df[
                "IndividualTreatmentEffect"
            ].mean()
        )

        result[
            "maximum_treatment_effect"
        ] = float(
            df[
                "IndividualTreatmentEffect"
            ].max()
        )

        result[
            "minimum_treatment_effect"
        ] = float(
            df[
                "IndividualTreatmentEffect"
            ].min()
        )

    # --------------------------------------------------------
    # Discount
    # --------------------------------------------------------

    if "RecommendedDiscount" in df.columns:

        result[
            "average_discount"
        ] = float(
            df[
                "RecommendedDiscount"
            ].mean()
        )

        result[
            "maximum_discount"
        ] = float(
            df[
                "RecommendedDiscount"
            ].max()
        )

    # --------------------------------------------------------
    # Prices
    # --------------------------------------------------------

    if "CurrentAveragePrice" in df.columns:

        result[
            "average_current_price"
        ] = float(
            df[
                "CurrentAveragePrice"
            ].mean()
        )

    if "RecommendedPrice" in df.columns:

        result[
            "average_recommended_price"
        ] = float(
            df[
                "RecommendedPrice"
            ].mean()
        )

    # --------------------------------------------------------
    # Revenue
    # --------------------------------------------------------

    if "RecommendedRevenue" in df.columns:

        result[
            "total_recommended_revenue"
        ] = float(
            df[
                "RecommendedRevenue"
            ].sum()
        )

    if "BaselineRevenue" in df.columns:

        result[
            "total_baseline_revenue"
        ] = float(
            df[
                "BaselineRevenue"
            ].sum()
        )

    return result


# ============================================================
# 17. SEARCH CUSTOMERS
# ============================================================

@app.get("/search")
def search_customers(
    customer_id: str = None,
    strategy: str = None
):

    if df.empty:

        raise HTTPException(
            status_code=500,
            detail="Dataset is not loaded."
        )

    result = df.copy()

    # --------------------------------------------------------
    # Search by customer ID
    # --------------------------------------------------------

    if customer_id:

        if "CustomerID" not in result.columns:

            raise HTTPException(
                status_code=500,
                detail="CustomerID column is missing."
            )

        result = result[
            result["CustomerID"]
            .astype(str)
            .str.contains(
                str(customer_id),
                case=False,
                na=False
            )
        ]

    # --------------------------------------------------------
    # Search by pricing strategy
    # --------------------------------------------------------

    if strategy:

        if "PricingStrategy" not in result.columns:

            raise HTTPException(
                status_code=500,
                detail=(
                    "PricingStrategy column "
                    "is missing."
                )
            )

        result = result[
            result["PricingStrategy"]
            .astype(str)
            .str.contains(
                strategy,
                case=False,
                na=False
            )
        ]

    records = []

    for _, row in result.iterrows():

        records.append(
            row_to_dict(row)
        )

    return {
        "count": len(records),
        "customers": records
    }


# ============================================================
# 18. STARTUP EVENT
# ============================================================

@app.on_event("startup")
def startup_event():

    print("")
    print("========================================")
    print("EconoCausal API Started")
    print("========================================")

    print(
        f"Dataset: {DATA_FILE}"
    )

    if df.empty:

        print(
            "WARNING: Dataset not loaded."
        )

    else:

        if "CustomerID" in df.columns:

            customers = df[
                "CustomerID"
            ].nunique()

        else:

            customers = len(df)

        print(
            f"Customers loaded: {customers}"
        )

        print(
            f"Rows loaded: {len(df)}"
        )

        print(
            "Dataset loaded successfully."
        )

    print("========================================")