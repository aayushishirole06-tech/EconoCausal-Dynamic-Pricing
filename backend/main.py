from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import pandas as pd
import numpy as np

app = FastAPI(
    title="EconoCausal Dynamic Pricing API",
    description="Dynamic pricing API using causal machine learning results",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "dynamic_pricing_recommendations.csv"
)

df = pd.DataFrame()


def convert_value(value):
    if pd.isna(value):
        return None

    if isinstance(value, (np.integer,)):
        return int(value)

    if isinstance(value, (np.floating,)):
        return float(value)

    return value


def row_to_dict(row):
    result = {}

    for column in row.index:
        result[column] = convert_value(row[column])

    return result


def load_dataset():
    global df

    try:
        df = pd.read_csv(DATA_FILE)
        df.columns = df.columns.str.strip()

        print("========================================")
        print("EconoCausal API Started")
        print("========================================")
        print("Dataset:", DATA_FILE)
        print("Rows:", len(df))
        print("Columns:", len(df.columns))

        if "CustomerID" in df.columns:
            print("Customers:", df["CustomerID"].nunique())

        print("Dataset loaded successfully.")
        print("========================================")

    except Exception as e:
        df = pd.DataFrame()
        print("Dataset loading error:", e)


load_dataset()


@app.get("/")
def root():
    return {
        "project": "EconoCausal",
        "application": "Dynamic Pricing System",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    if df.empty:
        return {
            "status": "warning",
            "dataset_loaded": False,
            "customers": 0
        }

    customers = 0

    if "CustomerID" in df.columns:
        customers = int(df["CustomerID"].nunique())
    else:
        customers = len(df)

    return {
        "status": "healthy",
        "dataset_loaded": True,
        "customers": customers
    }


@app.get("/dataset-info")
def dataset_info():
    if df.empty:
        raise HTTPException(
            status_code=500,
            detail="Dataset is not loaded."
        )

    customers = 0

    if "CustomerID" in df.columns:
        customers = int(df["CustomerID"].nunique())

    return {
        "rows": int(len(df)),
        "columns": df.columns.tolist(),
        "customers": customers,
        "file": str(DATA_FILE)
    }


@app.get("/customers")
def get_customers():
    if df.empty:
        raise HTTPException(
            status_code=500,
            detail="Dataset is not loaded."
        )

    records = []

    for _, row in df.iterrows():
        records.append(row_to_dict(row))

    return {
        "count": len(records),
        "customers": records
    }


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

    result = df[
        df["CustomerID"].astype(str) == str(customer_id)
    ]

    if result.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Customer {customer_id} was not found."
        )

    return row_to_dict(result.iloc[0])


@app.get("/customer/{customer_id}/pricing")
def get_customer_pricing(customer_id: str):
    if df.empty:
        raise HTTPException(
            status_code=500,
            detail="Dataset is not loaded."
        )

    result = df[
        df["CustomerID"].astype(str) == str(customer_id)
    ]

    if result.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Customer {customer_id} was not found."
        )

    row = result.iloc[0]

    fields = [
        "CustomerID",
        "IndividualTreatmentEffect",
        "AverageTreatmentEffect",
        "AveragePriceReduction",
        "CustomerResponse",
        "RecommendedDiscount",
        "PricingStrategy",
        "CurrentAveragePrice",
        "RecommendedPrice",
        "ExpectedRevenue",
        "RecommendedRevenue"
    ]

    pricing = {}

    for field in fields:
        if field in df.columns:
            pricing[field] = convert_value(row[field])

    return pricing


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
            detail="IndividualTreatmentEffect column is missing."
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
        records.append(row_to_dict(row))

    return {
        "count": len(records),
        "customers": records
    }


@app.get("/pricing-summary")
def pricing_summary():
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

    if "CustomerResponse" in df.columns:
        result["response_distribution"] = (
            df["CustomerResponse"]
            .value_counts()
            .to_dict()
        )

    if "RecommendedDiscount" in df.columns:
        result["discount_distribution"] = (
            df["RecommendedDiscount"]
            .value_counts()
            .sort_index()
            .to_dict()
        )

    if "PricingStrategy" in df.columns:
        result["pricing_strategies"] = (
            df["PricingStrategy"]
            .value_counts()
            .to_dict()
        )

    return result


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
        result["average_recommended_discount"] = float(
            df["RecommendedDiscount"].mean()
        )

    if "RecommendedPrice" in df.columns:
        result["average_recommended_price"] = float(
            df["RecommendedPrice"].mean()
        )

    if "RecommendedRevenue" in df.columns:
        result["total_recommended_revenue"] = float(
            df["RecommendedRevenue"].sum()
        )

    if "ExpectedRevenue" in df.columns:
        result["total_expected_revenue"] = float(
            df["ExpectedRevenue"].sum()
        )

    if "CustomerResponse" in df.columns:
        result["customer_response"] = (
            df["CustomerResponse"]
            .value_counts()
            .to_dict()
        )

    return result


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

    if customer_id:
        result = result[
            result["CustomerID"]
            .astype(str)
            .str.contains(
                str(customer_id),
                case=False,
                na=False
            )
        ]

    if strategy:
        if "PricingStrategy" not in result.columns:
            raise HTTPException(
                status_code=500,
                detail="PricingStrategy column is missing."
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
        records.append(row_to_dict(row))

    return {
        "count": len(records),
        "customers": records
    }