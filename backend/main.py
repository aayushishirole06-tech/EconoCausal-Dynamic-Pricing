from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# ECONOCAUSAL - DYNAMIC PRICING BACKEND
# ============================================================

app = FastAPI(
    title="EconoCausal Dynamic Pricing API",
    description="Customer-level causal dynamic pricing API",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ============================================================
# PROJECT PATH
# ============================================================

# main.py is inside:
# EconoCausal-Dynamic-Pricing/backend/
#
# parent.parent gives:
# EconoCausal-Dynamic-Pricing/

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "dynamic_pricing_recommendations.csv"
)


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():

    if not DATA_FILE.exists():

        print("\nERROR: Dataset not found!")
        print("Expected location:")
        print(DATA_FILE)

        return pd.DataFrame()

    try:

        data = pd.read_csv(DATA_FILE)

        if data.empty:

            print("\nWARNING: Dataset is empty!")

            return pd.DataFrame()

        data = data.replace(
            [np.inf, -np.inf],
            np.nan
        )

        data = data.drop_duplicates()

        data = data.reset_index(drop=True)

        print("\nDataset loaded successfully!")
        print("Rows:", len(data))
        print("Columns:", len(data.columns))

        return data

    except Exception as error:

        print(
            "\nERROR while loading dataset:",
            error
        )

        return pd.DataFrame()


df = load_dataset()


# ============================================================
# JSON VALUE CONVERSION
# ============================================================

def convert_value(value):

    if value is None:
        return None

    try:

        if pd.isna(value):
            return None

    except Exception:
        pass

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
# ROW TO DICTIONARY
# ============================================================

def row_to_dict(row):

    result = {}

    for column in row.index:

        result[column] = convert_value(
            row[column]
        )

    return result


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "project": "EconoCausal",
        "application": "Dynamic Pricing System",
        "status": "running",
        "version": "1.0.0",
        "dataset_loaded": not df.empty,
        "documentation": "/docs"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    if df.empty:

        return {
            "status": "warning",
            "dataset_loaded": False,
            "customers": 0,
            "message": "Pricing dataset is not loaded."
        }

    if "CustomerID" in df.columns:

        customer_count = int(
            df["CustomerID"].nunique()
        )

    else:

        customer_count = len(df)

    return {
        "status": "healthy",
        "dataset_loaded": True,
        "customers": customer_count,
        "rows": len(df)
    }


# ============================================================
# DATASET INFORMATION
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
        "columns": df.columns.tolist(),
        "customers": customer_count,
        "file": str(DATA_FILE)
    }


# ============================================================
# GET ALL CUSTOMERS
# ============================================================

@app.get("/customers")
def get_customers(
    limit: int = Query(
        100,
        ge=1,
        le=1000
    )
):

    if df.empty:

        raise HTTPException(
            status_code=500,
            detail="Dataset is not loaded."
        )

    result = df.head(limit)

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
# GET ONE CUSTOMER
# ============================================================

@app.get("/customer/{customer_id}")
def get_customer(
    customer_id: str
):

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
            detail=f"Customer {customer_id} was not found."
        )

    return row_to_dict(
        customer.iloc[0]
    )


# ============================================================
# CUSTOMER PRICING RECOMMENDATION
# ============================================================

@app.get("/customer/{customer_id}/pricing")
def customer_pricing(
    customer_id: str
):

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
            detail=f"Customer {customer_id} was not found."
        )

    row = customer.iloc[0]

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

        "CustomerProfile": {

            "TotalSpend": get_column(
                ["TotalSpend"]
            ),

            "TotalQuantity": get_column(
                ["TotalQuantity"]
            ),

            "NumberOfTransactions": get_column(
                ["NumberOfTransactions"]
            ),

            "AverageOrderValue": get_column(
                ["AverageOrderValue"]
            ),

            "AverageUnitPrice": get_column(
                ["AverageUnitPrice"]
            ),

            "RecencyDays": get_column(
                ["RecencyDays"]
            ),

            "SpendSegment": get_column(
                ["SpendSegment"]
            )
        },

        "CausalAnalysis": {

            "DiscountTreatment": get_column(
                ["DiscountTreatment"]
            ),

            "PurchaseOutcome": get_column(
                ["PurchaseOutcome"]
            ),

            "IndividualTreatmentEffect":
                get_column(
                    [
                        "IndividualTreatmentEffect",
                        "TreatmentEffect"
                    ]
                ),

            "CustomerResponse":
                get_column(
                    ["CustomerResponse"]
                )
        },

        "DynamicPricing": {

            "RecommendedDiscount":
                get_column(
                    [
                        "RecommendedDiscount",
                        "OptimalDiscount"
                    ]
                ),

            "PricingStrategy":
                get_column(
                    [
                        "PricingStrategy",
                        "OptimizationStrategy"
                    ]
                ),

            "CurrentPrice":
                get_column(
                    [
                        "CurrentAveragePrice",
                        "AverageUnitPrice"
                    ]
                ),

            "RecommendedPrice":
                get_column(
                    [
                        "RecommendedPrice",
                        "OptimalPrice"
                    ]
                ),

            "ExpectedRevenue":
                get_column(
                    [
                        "ExpectedRevenue",
                        "AdjustedExpectedRevenue",
                        "RecommendedRevenue"
                    ]
                )
        }
    }


# ============================================================
# HIGH RESPONSE CUSTOMERS
# ============================================================

@app.get("/customers/high-response")
def high_response_customers(
    limit: int = Query(
        20,
        ge=1,
        le=100
    )
):

    if df.empty:

        raise HTTPException(
            status_code=500,
            detail="Dataset is not loaded."
        )

    if "IndividualTreatmentEffect" not in df.columns:

        raise HTTPException(
            status_code=500,
            detail="IndividualTreatmentEffect column is missing."
        )

    result = df[
        df["IndividualTreatmentEffect"] > 0
    ].copy()

    result = result.sort_values(
        "IndividualTreatmentEffect",
        ascending=False
    ).head(limit)

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
# PRICING SUMMARY
# ============================================================

@app.get("/pricing-summary")
def pricing_summary():

    if df.empty:

        raise HTTPException(
            status_code=500,
            detail="Dataset is not loaded."
        )

    result = {}

    # Total customers
    if "CustomerID" in df.columns:

        result["total_customers"] = int(
            df["CustomerID"].nunique()
        )

    # Average treatment effect
    if "IndividualTreatmentEffect" in df.columns:

        result["average_treatment_effect"] = float(
            df["IndividualTreatmentEffect"].mean()
        )

    # Average discount
    if "RecommendedDiscount" in df.columns:

        result["average_recommended_discount"] = float(
            df["RecommendedDiscount"].mean()
        )

    # Average recommended price
    if "RecommendedPrice" in df.columns:

        result["average_recommended_price"] = float(
            df["RecommendedPrice"].mean()
        )

    # Expected revenue
    if "ExpectedRevenue" in df.columns:

        result["total_expected_revenue"] = float(
            df["ExpectedRevenue"].sum()
        )

    # Customer response
    if "CustomerResponse" in df.columns:

        result["customer_response_distribution"] = {
            str(key): int(value)
            for key, value
            in df["CustomerResponse"]
            .value_counts()
            .items()
        }

    # Pricing strategy
    if "PricingStrategy" in df.columns:

        result["pricing_strategy_distribution"] = {
            str(key): int(value)
            for key, value
            in df["PricingStrategy"]
            .value_counts()
            .items()
        }

    return result


# ============================================================
# STATISTICS
# ============================================================

@app.get("/statistics")
def statistics():

    if df.empty:

        raise HTTPException(
            status_code=500,
            detail="Dataset is not loaded."
        )

    result = {}

    if "CustomerID" in df.columns:

        result["total_customers"] = int(
            df["CustomerID"].nunique()
        )

    if "TotalSpend" in df.columns:

        result["total_spend"] = float(
            df["TotalSpend"].sum()
        )

        result["average_spend"] = float(
            df["TotalSpend"].mean()
        )

    if "TotalQuantity" in df.columns:

        result["total_quantity"] = float(
            df["TotalQuantity"].sum()
        )

    if "IndividualTreatmentEffect" in df.columns:

        result["average_treatment_effect"] = float(
            df["IndividualTreatmentEffect"].mean()
        )

        result["maximum_treatment_effect"] = float(
            df["IndividualTreatmentEffect"].max()
        )

        result["minimum_treatment_effect"] = float(
            df["IndividualTreatmentEffect"].min()
        )

    if "RecommendedDiscount" in df.columns:

        result["average_discount"] = float(
            df["RecommendedDiscount"].mean()
        )

        result["maximum_discount"] = float(
            df["RecommendedDiscount"].max()
        )

    if "CurrentAveragePrice" in df.columns:

        result["average_current_price"] = float(
            df["CurrentAveragePrice"].mean()
        )

    if "RecommendedPrice" in df.columns:

        result["average_recommended_price"] = float(
            df["RecommendedPrice"].mean()
        )

    if "ExpectedRevenue" in df.columns:

        result["total_expected_revenue"] = float(
            df["ExpectedRevenue"].sum()
        )

    return result


# ============================================================
# SEARCH CUSTOMERS
# ============================================================

@app.get("/search")
def search_customers(
    customer_id: str = None,
    strategy: str = None,
    response: str = None,
    segment: str = None,
    limit: int = Query(
        50,
        ge=1,
        le=500
    )
):

    if df.empty:

        raise HTTPException(
            status_code=500,
            detail="Dataset is not loaded."
        )

    result = df.copy()

    # Search by Customer ID
    if customer_id:

        if "CustomerID" in result.columns:

            result = result[
                result["CustomerID"]
                .astype(str)
                .str.contains(
                    str(customer_id),
                    case=False,
                    na=False
                )
            ]

    # Search by pricing strategy
    if strategy:

        if "PricingStrategy" in result.columns:

            result = result[
                result["PricingStrategy"]
                .astype(str)
                .str.contains(
                    strategy,
                    case=False,
                    na=False
                )
            ]

    # Search by customer response
    if response:

        if "CustomerResponse" in result.columns:

            result = result[
                result["CustomerResponse"]
                .astype(str)
                .str.contains(
                    response,
                    case=False,
                    na=False
                )
            ]

    # Search by spend segment
    if segment:

        if "SpendSegment" in result.columns:

            result = result[
                result["SpendSegment"]
                .astype(str)
                .str.contains(
                    segment,
                    case=False,
                    na=False
                )
            ]

    result = result.head(limit)

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
# RELOAD DATASET
# ============================================================

@app.post("/reload")
def reload_dataset():

    global df

    df = load_dataset()

    return {
        "message": "Dataset reload completed.",
        "dataset_loaded": not df.empty,
        "rows": len(df)
    }


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
def startup_event():

    print("\n")
    print("=" * 60)
    print("ECONOCAUSAL API STARTED")
    print("=" * 60)

    print("Dataset:")
    print(DATA_FILE)

    if df.empty:

        print("\nDataset Status: NOT LOADED")

    else:

        print("\nDataset Status: LOADED")
        print("Rows:", len(df))

        if "CustomerID" in df.columns:

            print(
                "Customers:",
                df["CustomerID"].nunique()
            )

    print("=" * 60)
    print("Swagger: http://127.0.0.1:8000/docs")
    print("=" * 60)