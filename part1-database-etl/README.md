# Part 1 – Database Design and ETL Pipeline (FlexiMart)

## Student Information

**Name:** Asima Maharana \
**Project:** FlexiMart Data Architecture  
**Part:** Part 1 – Database Design and ETL Pipeline  
**Database Used:** MySQL 8.0

---

## 1. Overview

This part of the project implements a complete **ETL (Extract, Transform, Load) pipeline** for FlexiMart, an e-commerce company. Raw CSV files containing customer, product, and sales data with intentional data quality issues are cleaned, validated, and loaded into a **normalized relational database (OLTP)**.

The final output is a reliable transactional database (`fleximart`) that supports accurate business reporting through SQL queries.

---

## 2. Objectives

- Ingest raw CSV data with real-world quality issues
- Clean and standardize inconsistent data
- Enforce referential integrity
- Load data into a normalized MySQL schema (3NF)
- Generate a data quality report
- Answer business questions using SQL

---

## 3. Input Data Files

Location: /data/

### Files Used

- `customers_raw.csv`
- `products_raw.csv`
- `sales_raw.csv`

### Data Quality Issues Present

- Missing mandatory values
- Duplicate records
- Inconsistent phone number formats
- Inconsistent category naming
- Invalid references between sales, customers, and products
- Mixed date formats

These issues are intentionally included and handled during transformation.

---

## 4. Database Schema (OLTP)

**Database Name:** `fleximart`

This schema follows **Third Normal Form (3NF)** and separates transactional data into logically independent entities.

### Tables

#### customers

```sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    city VARCHAR(50),
    registration_date DATE
);
```

#### products

```sql
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT DEFAULT 0
);
```

#### orders

```sql
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT DEFAULT 0
);
```

#### order_items

```sql
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

⚠️ Note:
There is no sales table. Sales data is decomposed into orders and order_items, which is the correct normalized design.

##

## 5. ETL Pipeline Design (etl_pipeline.py)

### 5.1 Extract

#### Reads all three CSV files using pandas

#### Validates file availability before processing

### 5.2 Transform

### Customers

    - Drops rows with missing email, first name, last name, or registration date

    - Removes duplicate customers based on email

    - Standardizes phone numbers to +91-XXXXXXXXXX

    - Converts dates to YYYY-MM-DD

### Products

    - Drops rows with missing product name, category, or price

    - Normalizes category names (case-insensitive)

    - Drops invalid prices (≤ 0 or > 100000)

    - Defaults missing stock quantities to 0

    - Removes duplicate products by (product_name, category)

### Sales

    - Drops rows with invalid dates

    - Drops sales referencing non-existent customers or products

    - Groups data by customer and order date

### Creates:

    - One row per order in orders

    - Multiple rows per order in order_items

    - Recalculates subtotals and total order amount

    - All transformations are deterministic and repeatable.

### 5.3 Load

#### Uses MySQL AUTO_INCREMENT for surrogate keys

#### Performs foreign key lookups from the database

#### Inserts data using controlled transactions

#### Ensures idempotent re-runs (duplicates ignored safely)

---

## 6. Data Quality Report

### After execution, the ETL pipeline generates:

    data_quality_report.txt

### Sample Output

---

    customers_read: 21
    customers_dropped_missing: 1
    customers_duplicates: 1
    customers_loaded: 19

    products_read: 20
    products_duplicates: 1
    products_loaded: 18

    sales_read: 31
    sales_invalid_customer: 2
    sales_invalid_product: 2
    orders_created: 18
    order_items_created: 27

---

## 7. Business Queries (business_queries.sql)

### Query 1: Customer Purchase History

    Customers with ≥ 2 orders

    Total spending > ₹5,000

    Uses JOIN, GROUP BY, HAVING

### Query 2: Product Sales Analysis

    Revenue and quantity sold by category

    Includes only categories with revenue > ₹10,000

## Query 3: Monthly Sales Trend

    Monthly revenue and order count for 2024

    Includes cumulative revenue using window functions

### All queries are written using correct aggregation grain (order_items) and validated against actual data.

---

## 8. How to Run

### Step 1: Create Database

    CREATE DATABASE fleximart;

### Step 2: Create Tables

    Run the schema SQL exactly as provided above.

### Step 3: Run ETL Pipeline

    cd part1-database-etl
    python etl_pipeline.py

### Step 4: Run Business Queries

#### Using MySQL Command Line Client:

    USE fleximart;
    SOURCE business_queries.sql;

---

## 9. Validation Checks

### Recommended verification queries:

    SELECT COUNT(*) FROM customers;
    SELECT COUNT(*) FROM products;
    SELECT COUNT(*) FROM orders;
    SELECT COUNT(*) FROM order_items;

### Ensure:

    - orders < order_items

    - No foreign key violations

    - Non-zero realistic counts

---

## 10. Key Learnings

    Designing ETL pipelines with real-world data quality issues

    Importance of normalization in OLTP systems

    Proper decomposition of sales data into orders and order items

    Writing reliable SQL analytics on normalized schemas

    Understanding the difference between OLTP and OLAP systems

---

## 11. Important Notes

    Raw sales data does not map directly to a database table

    No schema modifications were made beyond the provided specification

    All transformations are rule-based and justified

    This database is intended for transactions, not analytics (data warehouse is handled in Part 3)
