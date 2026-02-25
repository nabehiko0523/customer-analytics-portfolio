# Customer Analytics Portfolio

Data & Analytics implementations focused on CDP and marketing analytics.

## 🎯 Purpose
Demonstrating practical implementation of customer data analysis, segmentation, and BI solutions for CDP/BI.

## 📊 Projects

### 1. Marketing Analytics with SQL
**Location**: `sql/marketing_analysis/`

Implemented analyses:
- RFM Segmentation
- Cohort Retention Analysis
- Customer Lifetime Value (LTV)
- Purchase Funnel Analysis

### 2. Generate sample data
**Location**: `scripts/generate_sample_data.py`
Generate transaction sample data using python logarithmic distribution table

**Data spec**
- Number of customers : 100
- Number of orders : 500
- Duration : 2024/01 - 2025/02
- Category : Electronics, Clothing, Books, Food, Sports

**Tech Stack**: SQL (Snowflake dialect), dbt (planned)

## 🛠 Skills Demonstrated
- **Analytics**: Marketing analytics, customer segmentation
- **SQL**: Window functions, CTEs, complex aggregations
- **Platforms**: Snowflake, MS Fabric (QlikSense experience)
- **Domain**: Manufacturing, Customer Data Platform (CDP)

## 📝 Learning Journey
This portfolio is built as preparation for CDP/BI role, with focus on:
- Data platform architecture
- Marketing & customer analytics
- BI implementation best practices

## 📊 Analysis Implemented

### 1. RFM Analysis ✅
- Customer segmentation by Recency, Frequency, Monetary value
- Implementation: Python, DuckDB, Snowflake (ready)

### 2. Cohort Retention Analysis ✅
- Track customer retention by acquisition cohort
- Calculate monthly retention rates
- Implementation: Python, SQL

### 3. Customer Lifetime Value (LTV) ✅
- Predict 12-month and 24-month customer value
- Segment customers by predicted LTV
- Churn risk assessment
- Implementation: Python, SQL

## 🛠 Platform Support

| Platform | Status | Use Case | Performance |
|----------|--------|----------|-------------|
| **Python (Pandas)** | ✅ Implemented | Local development, prototyping | ~500ms (500 rows) |
| **DuckDB** | ✅ Implemented | Local SQL execution, testing | ~200ms (500 rows) |
| **Snowflake** | ✅ **Implemented** | **Production deployment** | **1.4s (500 rows)** |
| **BigQuery** | 📋 Planned | GCP projects | TBD |

### Snowflake Implementation

- **Database:** CUSTOMER_ANALYTICS
- **Tables:** TRANSACTIONS (500 rows)
- **Analyses:** RFM Segmentation
- **Screenshots:** [docs/screenshots/snowflake_*.png](docs/screenshots/)
- **Setup Guide:** [docs/snowflake_setup.md](docs/snowflake_setup.md)

**Key Features:**
- ✅ Enterprise-grade data warehouse
- ✅ Scalable for production workloads
- ✅ Result consistency across all platforms
- ✅ Cloud-native architecture

## 📈 Results

Sample analysis outputs available in `data/` folder:
- `rfm_results.csv` - Customer segmentation
- `cohort_retention_results.csv` - Retention analysis
- `ltv_analysis_results.csv` - Lifetime value predictions

# Sales forecasting model

## Background

Added Data driven sales forecasting model.

## Issue
- Sales planning is based on experiencem, not algorithm.
- No seasonality consideration
- Weak connection to inventory planning in terms of data.

## Approach

### Data
- Sample data generation by 3 years monthly sales result.
- Sales terend by product categories

### Features
- Trend
- Seasonality

### Model
- Liner Regression
- Evaluation indicator: MAE, RMSE, MAPE

## How to implement
```bash
# Generate sample data 
python scripts/generate_sales_data.py

# Implemet forecasting model
python scripts/sales_forecast_model.py
```

---
*Last Updated: [2026/02/25]*
