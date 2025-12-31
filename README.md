# FlexiMart Data Architecture Project

## Student Information

**Name:** Asima Maharana 
**Project Title:** FlexiMart – End-to-End Data Architecture  
**Technologies:** MySQL, MongoDB, Python  
**Architecture Type:** Hybrid (OLTP + NoSQL + OLAP)

---

## 1. Project Overview

FlexiMart is a simulated e-commerce data architecture project designed to demonstrate the complete lifecycle of enterprise data handling. The project covers:

- Transactional data storage (OLTP)
- Data cleaning and ETL pipelines
- NoSQL usage for flexible product catalogs
- Data warehouse design for analytical reporting

The architecture follows **industry best practices** by separating transactional workloads, flexible document storage, and analytical processing into independent systems.

---

## 2. High-Level Architecture

# FlexiMart Data Architecture Project

## Student Information

**Name:** Priyansh Awasthi  
**Project Title:** FlexiMart – End-to-End Data Architecture  
**Technologies:** MySQL, MongoDB, Python  
**Architecture Type:** Hybrid (OLTP + NoSQL + OLAP)

---

## 1. Project Overview

FlexiMart is a simulated e-commerce data architecture project designed to demonstrate the complete lifecycle of enterprise data handling. The project covers:

- Transactional data storage (OLTP)
- Data cleaning and ETL pipelines
- NoSQL usage for flexible product catalogs
- Data warehouse design for analytical reporting

The architecture follows **industry best practices** by separating transactional workloads, flexible document storage, and analytical processing into independent systems.

---

## 2. High-Level Architecture

    Raw CSV Files
        ↓
    Python ETL
        ↓
    MySQL (OLTP)
        ↓
    Python DW ETL
        ↓
    MySQL Data Warehouse (OLAP)

#### MongoDB (NoSQL) → Product Catalog & Reviews

#### Each layer serves a **distinct purpose** and is not overloaded with responsibilities.

---

## 3. Project Structure

fleximart-data-architecture \
│ \
├── data \
│ ├── customers_raw.csv \
│ ├── products_raw.csv \
│ └── sales_raw.csv \
│ \
├── part1-database-etl \
│ ├── README.md \
│ ├── etl_pipeline.py \
│ ├── business_queries.sql \
│ ├── schema_documentation.md \
│ └── data_quality_report.txt \
│ \
├── part2-nosql \
│ ├── README.md \
│ ├── nosql_analysis.md \
│ ├── mongodb_operations.js \
│ └── products_catalog.json \
│ \
├── part3-data-warehouse \
│ ├── README.md \
│ ├── dw_schema.sql \
│ ├── dw_etl.py \
│ ├── dw_queries.sql \
│ └── star_schema_documentation.md \
│ \
└── README.md

---

## 4. Part 1 – OLTP Database & ETL (MySQL)

### Purpose

To design a **normalized transactional database** and build an ETL pipeline that cleans and loads raw CSV data.

### Key Features

- MySQL OLTP schema in **3NF**
- Python ETL for customers, products, and sales
- Data validation and deduplication
- Referential integrity enforcement
- Business SQL queries for reporting

### Output

- Database: `fleximart`
- Tables: `customers`, `products`, `orders`, `order_items`
- Data quality report
- Business query results

📁 See: `part1-database-etl/README.md`

---

## 5. Part 2 – NoSQL Implementation (MongoDB)

### Purpose

To demonstrate why **NoSQL** is suitable for flexible product catalogs with heterogeneous attributes and embedded data.

### Key Features

- MongoDB 6.0 Community Server
- Document-based product catalog
- Embedded reviews
- Flexible schema using nested documents
- Aggregation pipelines for analytics

### Output

- Database: `fleximart_nosql`
- Collection: `products`
- CRUD and aggregation operations executed via `mongosh`

📁 See: `part2-nosql/README.md`

---

## 6. Part 3 – Data Warehouse (OLAP)

### Purpose

To design and populate a **data warehouse** optimized for analytical queries and historical reporting.

### Key Features

- Separate warehouse database (`fleximart_dw`)
- **Star schema** design
- Dimension tables: customer, product, date
- Fact table: sales
- Python-based ETL from OLTP → OLAP
- Analytical SQL queries

### Output

- Category-wise sales analysis
- Monthly and daily sales trends
- Top customers by revenue
- Product-level performance metrics

📁 See: `part3-data-warehouse/README.md`

---

## 7. Key Design Decisions

- **Separation of Concerns:**  
  OLTP, NoSQL, and OLAP systems are strictly separated.

- **Star Schema for Analytics:**  
  Simplifies queries and improves aggregation performance.

- **Python ETL:**  
  Provides control, validation, and repeatability across pipelines.

- **MongoDB for Flexibility:**  
  Used only where relational schemas become restrictive.

---

## 8. Technologies Used

| Layer          | Technology                |
| -------------- | ------------------------- |
| OLTP Database  | MySQL 8.0                 |
| ETL            | Python                    |
| NoSQL          | MongoDB 6.0               |
| Data Warehouse | MySQL (Star Schema)       |
| Scripting      | SQL, JavaScript (mongosh) |

---

## 9. Final Status

| Module                  | Status      |
| ----------------------- | ----------- |
| Part 1 – Database & ETL | ✅ Complete |
| Part 2 – NoSQL          | ✅ Complete |
| Part 3 – Data Warehouse | ✅ Complete |

---

## 10. Conclusion

This project demonstrates a complete, real-world data architecture pipeline, covering transactional processing, flexible document storage, and analytical reporting. Each component is designed using appropriate technologies and architectural principles, ensuring scalability, maintainability, and correctness.

**The project is complete and ready for evaluation.**
