# Star Schema Design – FlexiMart Data Warehouse

## Section 1: Schema Overview

The FlexiMart Data Warehouse is designed using a **Star Schema** to support analytical reporting and historical analysis of sales data. The schema consists of **one central fact table** surrounded by **three dimension tables**.

---

### FACT TABLE: fact_sales

**Business Process:** Sales Transactions  
**Grain:** One row per product per order line item

Each record in the fact table represents the sale of a single product in a specific order on a specific date.

#### Measures (Numeric Facts)

- **quantity_sold:** Number of units sold
- **unit_price:** Price per unit at the time of sale
- **discount_amount:** Discount applied to the sale
- **total_amount:** Final sales amount  
  _(quantity_sold × unit_price − discount_amount)_

#### Foreign Keys

- **date_key** → dim_date
- **product_key** → dim_product
- **customer_key** → dim_customer

---

### DIMENSION TABLE: dim_date

**Purpose:** Supports time-based analysis and reporting  
**Type:** Conformed Dimension

#### Attributes

- **date_key (PK):** Surrogate key in YYYYMMDD format
- **full_date:** Actual calendar date
- **day_of_week:** Monday, Tuesday, etc.
- **day_of_month:** Numeric day (1–31)
- **month:** Numeric month (1–12)
- **month_name:** January, February, etc.
- **quarter:** Q1, Q2, Q3, Q4
- **year:** Calendar year
- **is_weekend:** Boolean flag indicating weekend

---

### DIMENSION TABLE: dim_product

**Purpose:** Enables product and category-level analysis

#### Attributes

- **product_key (PK):** Surrogate key
- **product_id:** Business product identifier
- **product_name:** Name of the product
- **category:** Product category (Electronics, Fashion, etc.)
- **subcategory:** Product subcategory
- **unit_price:** Standard product price

---

### DIMENSION TABLE: dim_customer

**Purpose:** Enables customer-centric sales analysis

#### Attributes

- **customer_key (PK):** Surrogate key
- **customer_id:** Business customer identifier
- **customer_name:** Full name of the customer
- **city:** Customer city
- **state:** Customer state
- **customer_segment:** Segment such as Retail, Premium, Corporate

---

## Section 2: Design Decisions (Granularity, Keys, Analytics)

The data warehouse uses a **transaction line-item level granularity**, where each row in the fact table represents a single product sold within an order. This level of detail allows maximum analytical flexibility, enabling drill-down analysis from yearly sales down to individual products and customers.

**Surrogate keys** are used instead of natural keys to ensure stability and performance. Natural keys such as product IDs or customer IDs can change over time, whereas surrogate keys remain immutable and simplify joins. Surrogate keys also improve query performance by using compact integer values.

The star schema design supports **drill-down and roll-up operations** efficiently. Analysts can roll up data to higher levels such as month or category, or drill down to specific dates, products, or customers using dimension attributes. This structure minimizes join complexity and is optimized for OLAP workloads, making it ideal for business intelligence and reporting scenarios.

---

## Section 3: Sample Data Flow (Transaction to Warehouse)

### Source Transaction (OLTP System)

- **Order ID:** 101
- **Customer:** John Doe
- **City:** Mumbai
- **Product:** Laptop
- **Quantity:** 2
- **Unit Price:** ₹50,000
- **Order Date:** 2024-01-15

---

### Data Warehouse Representation

#### dim_date

    date_key: 20240115
    full_date: 2024-01-15
    month: 1
    month_name: January
    quarter: Q1
    year: 2024
    is_weekend: false

#### dim_product

    product_key: 5
    product_name: Laptop
    category: Electronics
    unit_price: 50000

#### fact_sales

    date_key: 20240115
    product_key: 5
    customer_key: 12
    quantity_sold: 2
    unit_price: 50000
    discount_amount: 0
    total_amount: 100000

###

This example demonstrates how a single transactional sale is transformed into dimensional records and a fact record in the data warehouse, enabling efficient analytical queries.
