# Snowflake Environment setup

## account info

- **Edition:** Enterprise Trial
- **Cloud Provider:** AWS
- **Region:** US East (N. Virginia)

## Database structure
```
CUSTOMER_ANALYTICS/
└── PUBLIC/
    └── TRANSACTIONS
        - 500 rows
        - Columns: customer_id, order_id, order_date, order_amount, product_category
```

## Contents of implementation

### 1. Data loas

- Source: `data/sample_transactions.csv`
- Method: Snowflake Web UI Upload
- Duration: < 1 min
- Status: ✅ Success

### 2. RFM analysis

**SQL:** `sql/snowflake/01_rfm_segmentation.sql`

**Duration:** 0.298 sec

**Results:**
- Customers: 97人
- Segment: 8種類
- Data quality: 100%（No null）

### 3. Results comparison

| Platform | Duration | Results |
|----------------|---------|------|
| Python (Pandas) | ~500ms | ✅  |
| DuckDB | ~200ms | ✅ |
| **Snowflake** | **0.298s** | ✅ |

**Learnings:**
- 

## Next steps

- [ ] Implement cohort analysis on Snowflake
- [ ] Implemet LTV analysis on Snowflake
- [ ] dbt pipeline structure
- [ ] Tableau/Power BI

---

**Crated on:** 2025-02-17
**Last update on:** 2025-02-25