"""FastAPI Backend for Business Analytics Dashboard.

This module provides REST API endpoints to serve processed data
for the frontend dashboard visualization.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Analytics API", version="1.0.0")

# CORS configuration - restrict to specific origins
ALLOWED_ORIGINS = [
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Data paths
BASE_DIR = Path(__file__).parent.parent
DATA = BASE_DIR / "data" / "processed"


# Pydantic response models for type safety
class RevenueRecord(BaseModel):
    """Monthly revenue data."""
    order_year_month: str
    amount: float


class CustomerRecord(BaseModel):
    """Top customer data."""
    customer_id: int
    name: str
    region: str
    total_spend: float
    churned: Optional[bool] = False


class CategoryRecord(BaseModel):
    """Product category performance."""
    category: str
    total_revenue: float
    avg_order_value: float
    number_of_orders: int


class RegionRecord(BaseModel):
    """Regional analysis data."""
    region: str
    customers: int
    orders: int
    revenue: float
    avg_revenue_per_customer: float


def read_csv_safe(file_name: str) -> pd.DataFrame:
    """Safely load CSV with validation and error handling.
    
    Args:
        file_name: Name of CSV file in processed data directory.
        
    Returns:
        pd.DataFrame: Loaded and validated data.
        
    Raises:
        HTTPException: If file not found or data invalid.
    """
    file_path = DATA / file_name

    if not file_path.exists():
        logger.error(f"Data file not found: {file_path}")
        raise HTTPException(status_code=404, detail=f"Data file '{file_name}' not found")

    try:
        df = pd.read_csv(file_path)
        
        # Log data quality warnings
        if df.isnull().any().any():
            logger.warning(f"Missing values in {file_name}: {df.isnull().sum().to_dict()}")
        
        # Replace NaN and infinite values with 0
        df = df.fillna(0)
        df = df.replace([float("inf"), float("-inf")], 0)
        
        if df.empty:
            logger.warning(f"Empty dataframe from {file_name}")
            raise HTTPException(status_code=500, detail=f"No data in '{file_name}'")
        
        return df

    except pd.errors.EmptyDataError:
        logger.error(f"Empty data file: {file_path}")
        raise HTTPException(status_code=500, detail=f"Data file '{file_name}' is empty")
    except Exception as e:
        logger.error(f"Error reading {file_path}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error reading data: {str(e)}")


@app.get("/health")
def health() -> dict:
    """Health check endpoint.
    
    Returns:
        dict: Status message.
    """
    return {"status": "ok"}


@app.get("/api/revenue", response_model=List[RevenueRecord])
def get_revenue() -> List[dict]:
    """Get monthly revenue trend.
    
    Returns:
        List[dict]: Monthly revenue records.
    """
    df = read_csv_safe("monthly_revenue.csv")
    logger.info(f"Retrieved {len(df)} revenue records")
    return df.to_dict(orient="records")


@app.get("/api/top-customers", response_model=List[CustomerRecord])
def get_top_customers() -> List[dict]:
    """Get top 10 customers by spend.
    
    Returns:
        List[dict]: Top customer records with churn status.
    """
    df = read_csv_safe("top_customers.csv")
    logger.info(f"Retrieved {len(df)} customer records")
    return df.to_dict(orient="records")


@app.get("/api/categories", response_model=List[CategoryRecord])
def get_categories() -> List[dict]:
    """Get category performance metrics.
    
    Returns:
        List[dict]: Category performance records.
    """
    df = read_csv_safe("category_performance.csv")
    logger.info(f"Retrieved {len(df)} category records")
    return df.to_dict(orient="records")


@app.get("/api/regions", response_model=List[RegionRecord])
def get_regions() -> List[dict]:
    """Get regional analysis metrics.
    
    Returns:
        List[dict]: Regional analysis records.
    """
    df = read_csv_safe("regional_analysis.csv")
    logger.info(f"Retrieved {len(df)} region records")
    return df.to_dict(orient="records")