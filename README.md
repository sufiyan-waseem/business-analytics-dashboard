# Business Analytics Dashboard - Full Stack Application

## Overview

A comprehensive end-to-end data pipeline and analytics dashboard that ingests raw customer and order data, performs advanced cleaning and analysis, and visualizes insights through an interactive web-based dashboard.

**Key Features:**

- ✅ Automated data cleaning and validation
- ✅ Multi-dataset merging with join validation
- ✅ Five business intelligence reports
- ✅ RESTful API backend
- ✅ Responsive interactive dashboard
- ✅ Production-grade error handling

---

## Tech Stack

| Layer                   | Technology         | Version      |
| ----------------------- | ------------------ | ------------ |
| **Backend**             | FastAPI            | >=0.104.0    |
| **Server**              | Uvicorn            | >=0.24.0     |
| **Data Processing**     | Pandas             | >=2.0.0      |
| **Numeric Computation** | NumPy              | >=1.24.0     |
| **Frontend**            | HTML5 + JavaScript | -            |
| **Visualization**       | Chart.js           | Latest (CDN) |

---

## Project Structure

```
.
├── clean_data.py              # Data cleaning pipeline
├── analyze.py                 # Data analysis & aggregations
├── README.md                  # This file
│
├── backend/
│   ├── main.py               # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   └── __pycache__/          # Compiled Python files
│
├── frontend/
│   └── index.html            # Interactive dashboard UI
│
└── data/
    ├── raw/
    │   ├── customers.csv     # Raw customer records
    │   ├── orders.csv        # Raw order transactions
    │   └── products.csv      # Product catalog
    │
    └── processed/
        ├── customers_clean.csv              # Cleaned customers
        ├── orders_clean.csv                 # Cleaned orders
        ├── monthly_revenue.csv              # Revenue aggregation
        ├── top_customers.csv                # Top 10 customers + churn
        ├── category_performance.csv         # Category metrics
        └── regional_analysis.csv            # Regional KPIs
```

---

## Installation & Setup

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### Step 2: Clean Raw Data

Run the data cleaning pipeline:

```bash
python clean_data.py
```

**Output:**

- `data/processed/customers_clean.csv` - Deduplicated, validated customers
- `data/processed/orders_clean.csv` - Cleaned, standardized orders

**Processing includes:**

- Duplicate removal (keep latest for customers)
- Email validation & normalization
- Date parsing (3 supported formats)
- Status normalization
- Missing value handling

### Step 3: Generate Analysis Reports

Run the analysis pipeline:

```bash
python analyze.py
```

**Output (5 CSV reports):**

1. `monthly_revenue.csv` - Revenue trend by month
2. `top_customers.csv` - Top 10 customers + 90-day churn flag
3. `category_performance.csv` - Revenue, AOV, order count by category
4. `regional_analysis.csv` - Regional KPIs
5. Plus merge validation logging

### Step 4: Start Backend API

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Step 5: View Dashboard

Open a browser and navigate to:

```
file:///[PATH_TO_PROJECT]/frontend/index.html
```

Or if serving HTML through backend:

```
http://localhost:8000/frontend/index.html
```

---

## API Documentation

### Base URL

```
http://localhost:8000
```

### Endpoints

#### 1. Health Check

```http
GET /health
```

**Response:**

```json
{
  "status": "ok"
}
```

---

#### 2. Monthly Revenue Trend

```http
GET /api/revenue
```

**Response:**

```json
[
  {
    "order_year_month": "2024-01",
    "amount": 15234.5
  },
  {
    "order_year_month": "2024-02",
    "amount": 18901.75
  }
]
```

**Use Case:** Revenue trend analysis, forecasting, performance tracking

---

#### 3. Top 10 Customers (with Churn)

```http
GET /api/top-customers
```

**Response:**

```json
[
  {
    "customer_id": 101,
    "name": "Acme Corp",
    "region": "North",
    "total_spend": 45230.0,
    "churned": false
  },
  {
    "customer_id": 205,
    "name": "TechStart Inc",
    "region": "South",
    "total_spend": 32100.5,
    "churned": true
  }
]
```

**Churn Definition:** No completed orders in the last 90 days

---

#### 4. Category Performance

```http
GET /api/categories
```

**Response:**

```json
[
  {
    "category": "Electronics",
    "total_revenue": 125450.75,
    "avg_order_value": 850.5,
    "number_of_orders": 147
  }
]
```

**Metrics:**

- `total_revenue`: Sum of all completed orders
- `avg_order_value`: Mean order amount
- `number_of_orders`: Count of completed orders

---

#### 5. Regional Analysis

```http
GET /api/regions
```

**Response:**

```json
[
  {
    "region": "North",
    "customers": 45,
    "orders": 320,
    "revenue": 98750.5,
    "avg_revenue_per_customer": 2194.46
  }
]
```

**Metrics for each region:**

- `customers`: Unique customer count
- `orders`: Total order count (all statuses)
- `revenue`: Total revenue from all orders
- `avg_revenue_per_customer`: Revenue / unique customers

---

### Error Handling

All endpoints return appropriate HTTP status codes:

| Status | Scenario                                   |
| ------ | ------------------------------------------ |
| 200    | ✅ Successful response                     |
| 404    | ❌ Data file not found                     |
| 500    | ❌ Server error (invalid data, empty file) |

**Error Response Example:**

```json
{
  "detail": "Data file 'monthly_revenue.csv' not found"
}
```

---

## Data Pipeline Workflow

```
┌─────────────────────────────────────────────────────────┐
│                   RAW DATA SOURCES                       │
├────────────┬────────────────┬──────────────────────────┤
│ customers  │     orders     │      products            │
│ .csv       │     .csv       │      .csv                │
└────────────┴────────────────┴──────────────────────────┘
             ↓
  ┌──────────────────────────┐
  │   clean_data.py          │
  │  - Deduplicate           │
  │  - Validate              │
  │  - Parse dates           │
  │  - Normalize             │
  └──────────────────────────┘
             ↓
┌────────────────────────────────────────┐
│    PROCESSED DATA                      │
├──────────────┬──────────────────────────┤
│customers_clean.csv  │  orders_clean.csv │
└──────────────┴──────────────────────────┘
             ↓
  ┌──────────────────────────┐
  │   analyze.py             │
  │  - Merge datasets        │
  │  - Aggregate metrics     │
  │  - Calculate churn       │
  └──────────────────────────┘
             ↓
├──────────────────────────────────────────────────────────┤
│            5 ANALYSIS OUTPUTS (CSVs)                      │
├──────────┬──────────┬──────────┬──────────┬──────────────┤
│ monthly_ │   top_   │ category │ regional │              │
│ revenue  │customers │_perf     │_analysis │              │
└──────────┴──────────┴──────────┴──────────┴──────────────┘
             ↓
  ┌──────────────────────────┐
  │   FastAPI Backend        │
  │   /api/revenue           │
  │   /api/top-customers     │
  │   /api/categories        │
  │   /api/regions           │
  └──────────────────────────┘
             ↓
  ┌──────────────────────────┐
  │   Frontend Dashboard     │
  │   - Charts               │
  │   - Tables               │
  │   - Real-time updates    │
  └──────────────────────────┘
```

---

## Data Cleaning Rules

### Customers Dataset

| Rule            | Action                                                  |
| --------------- | ------------------------------------------------------- |
| Duplicates      | Keep latest `signup_date` per `customer_id`             |
| Emails          | Lowercase + validate (contains @ and .)                 |
| Names/Regions   | Strip whitespace                                        |
| Missing Regions | Fill with `"Unknown"`                                   |
| Signup Date     | Parse formats: YYYY-MM-DD; replace unparseable with NaT |

### Orders Dataset

| Rule           | Action                                                           |
| -------------- | ---------------------------------------------------------------- |
| Order Date     | Parse 3 formats: YYYY-MM-DD, DD/MM/YYYY, MM-DD-YYYY              |
| Both IDs Null  | Drop row (unrecoverable)                                         |
| Missing Amount | Fill with median per product                                     |
| Status         | Normalize: `done`→`completed`, `canceled`→`cancelled`, lowercase |
| Year-Month     | Extract from `order_date` (YYYY-MM format)                       |

---

## Key Assumptions

1. **Date Parsing:**
   - Orders support 3 date formats: YYYY-MM-DD, DD/MM/YYYY, MM-DD-YYYY
   - Unparseable dates become `NaT` (Not a Time)

2. **Churn Definition:**
   - Customer churned if no **completed order** in last 90 days
   - Based on latest `order_date` in dataset

3. **Data Joins:**
   - Orders LEFT JOIN Customers (preserve unmatched orders)
   - All results LEFT JOIN Products by `product_name`
   - Unmatched customers/products get `NaN` values

4. **Revenue Calculations:**
   - Only **completed** orders count for revenue
   - Monthly revenue excludes cancelled/pending/refunded orders
   - Top customers use completed orders only

5. **Regional Metrics:**
   - Include ALL orders (not filtered to completed)
   - Allows visibility into pending/problematic regions

6. **API Response:**
   - `NaN` and `Infinity` values replaced with `0`
   - Empty dataframes trigger HTTP 500 error

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'pandas'`

**Solution:**

```bash
pip install -r backend/requirements.txt
```

### Issue: `FileNotFoundError: data/processed/customers_clean.csv`

**Solution:** Run `clean_data.py` first, then `analyze.py`

```bash
python clean_data.py
python analyze.py
```

### Issue: Dashboard shows "Failed to load dashboard data"

**Solution:** Check backend is running on `http://127.0.0.1:8000`

```bash
cd backend
uvicorn main:app --reload
```

### Issue: CORS error in browser console

**Solution:** Ensure frontend is accessed from allowed origin:

- http://localhost:5000
- http://127.0.0.1:5000
- http://localhost:3000
- http://127.0.0.1:3000

---

## Performance Notes

- **CSV reads:** Files loaded fresh on each API request (no caching)
- **Recommended:** For datasets > 1M rows, consider:
  - In-memory caching (Redis)
  - Database backend (PostgreSQL)
  - Pagination on large responses

---

## Sample Commands (Copy-Paste)

**Full pipeline (4-step):**

```bash
# 1. Clean data
python clean_data.py

# 2. Analyze data
python analyze.py

# 3. Start backend
cd backend && uvicorn main:app --reload

# 4. In browser, open frontend
# file:///[PATH]/frontend/index.html
```

**Test API endpoints (curl):**

```bash
# Health check
curl http://localhost:8000/health

# Get revenue data
curl http://localhost:8000/api/revenue | jq

# Get top customers
curl http://localhost:8000/api/top-customers | jq

# Get categories
curl http://localhost:8000/api/categories | jq

# Get regions
curl http://localhost:8000/api/regions | jq
```

---

## Files Modified for Quality Improvements

✅ **clean_data.py**

- Added module/function docstrings
- Added type hints (str, pd.DataFrame)
- Error handling with meaningful messages
- Automatic `data/processed/` directory creation

✅ **analyze.py**

- Added module/function docstrings
- Wrapped in `main()` function
- Merge validation logging
- Error handling for missing files

✅ **backend/main.py**

- Added Pydantic response models
- Type hints on all functions
- Improved CORS security (restricted origins)
- Comprehensive logging
- Better error messages

✅ **frontend/index.html**

- Mobile-responsive CSS (375px - 1280px+)
- Number formatting (currency, commas)
- Churn status with color coding
- XSS-safe table generation
- Better UX with icons and colors

✅ **backend/requirements.txt**

- Version pinning for all dependencies
- Ensures reproducibility

---

## Author

Sufiyan Waseem

---

## License

Open source for educational purposes

---

**Last Updated:** April 2026  
**Version:** 1.0.0
