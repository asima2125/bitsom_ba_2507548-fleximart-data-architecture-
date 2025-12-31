# Part 3 – Data Warehouse Implementation (FlexiMart)

## Overview

This part of the project implements a **data warehouse** for FlexiMart using a star schema. Data is extracted from the OLTP database (`fleximart`) and loaded into an analytical database (`fleximart_dw`) using a Python-based ETL process.

The data warehouse supports business intelligence queries such as sales trends, top customers, and category-level revenue analysis.

---

## Objectives

- Design a star schema for analytical workloads
- Separate OLTP and OLAP systems
- Load data into the warehouse using Python ETL
- Perform analytical queries on historical data

---

## Technologies Used

- MySQL 8.0
- Python 3
- mysql-connector-python

---

## Schema Design

The warehouse follows a star schema with:

- **Fact table:** fact_sales
- **Dimensions:** dim_customer, dim_product, dim_date

Surrogate keys are used for all dimension tables.

---

## ETL Process

The Python ETL script (`dw_etl.py`):

- Extracts data from OLTP tables
- Loads dimension tables first
- Resolves surrogate keys
- Loads fact table with sales measures
- Is idempotent and safe to rerun

---

## Analytical Queries

Analytical queries are defined in `analytics_queries.sql` and include:

- Sales by category
- Monthly and daily sales trends
- Top customers by revenue
- Product-level sales performance

---

## How to Run

### 1. Create Warehouse Schema

```bash
mysql -u root -p < warehouse_schema.sql
```

### 2. Run Warehouse ETL

```bash
python dw_etl.py
```

### 3. Execute Analytical Queries

```bash
mysql -u root -p <YOUR_PASSWORD> fleximart_dw < analytics_queries.sql
```

---

# 🎯 FINAL STATUS — ASSIGNMENT COMPLETE

| Part                    | Status |
| ----------------------- | ------ |
| Part 1 – OLTP + ETL     | ✅     |
| Part 2 – NoSQL          | ✅     |
| Part 3 – Data Warehouse | ✅     |
