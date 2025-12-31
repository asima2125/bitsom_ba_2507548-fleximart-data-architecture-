import mysql.connector
from datetime import datetime
import logging

# ---------------------------
# CONFIG
# ---------------------------
OLTP_DB = {
    "host": "localhost",
    "user": "root",
    "password": "asima",
    "database": "fleximart"
}

DW_DB = {
    "host": "localhost",
    "user": "root",
    "password": "asima",
    "database": "fleximart_dw"
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# ---------------------------
# DB CONNECTIONS
# ---------------------------
def get_connection(cfg):
    return mysql.connector.connect(**cfg)


# ---------------------------
# LOAD DIM CUSTOMER
# ---------------------------
def load_dim_customer(oltp_cur, dw_cur):
    logging.info("Loading dim_customer")

    oltp_cur.execute("""
        SELECT customer_id, CONCAT(first_name, ' ', last_name) AS full_name, email, city
        FROM customers
    """)
    rows = oltp_cur.fetchall()

    for r in rows:
        dw_cur.execute("""
            INSERT IGNORE INTO dim_customer (customer_id, full_name, email, city)
            VALUES (%s, %s, %s, %s)
        """, r)


# ---------------------------
# LOAD DIM PRODUCT
# ---------------------------
def load_dim_product(oltp_cur, dw_cur):
    logging.info("Loading dim_product")

    oltp_cur.execute("""
        SELECT product_id, product_name, category, price
        FROM products
    """)
    rows = oltp_cur.fetchall()

    for r in rows:
        dw_cur.execute("""
            INSERT IGNORE INTO dim_product (product_id, product_name, category, price)
            VALUES (%s, %s, %s, %s)
        """, r)


# ---------------------------
# LOAD DIM DATE
# ---------------------------
def load_dim_date(oltp_cur, dw_cur):
    logging.info("Loading dim_date")

    oltp_cur.execute("""
        SELECT DISTINCT order_date
        FROM orders
    """)
    dates = oltp_cur.fetchall()

    for (d,) in dates:
        dw_cur.execute("""
            INSERT IGNORE INTO dim_date (full_date, day, month, month_name, year)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            d,
            d.day,
            d.month,
            d.strftime("%B"),
            d.year
        ))


# ---------------------------
# LOAD FACT SALES
# ---------------------------
def load_fact_sales(oltp_cur, dw_cur):
    logging.info("Loading fact_sales")

    oltp_cur.execute("""
        SELECT 
            o.customer_id,
            oi.product_id,
            o.order_date,
            oi.quantity,
            oi.subtotal
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
    """)
    rows = oltp_cur.fetchall()

    for customer_id, product_id, order_date, qty, amount in rows:
        # Resolve dimension keys
        dw_cur.execute("SELECT customer_key FROM dim_customer WHERE customer_id = %s", (customer_id,))
        customer_key = dw_cur.fetchone()[0]

        dw_cur.execute("SELECT product_key FROM dim_product WHERE product_id = %s", (product_id,))
        product_key = dw_cur.fetchone()[0]

        dw_cur.execute("SELECT date_key FROM dim_date WHERE full_date = %s", (order_date,))
        date_key = dw_cur.fetchone()[0]

        dw_cur.execute("""
            INSERT INTO fact_sales (customer_key, product_key, date_key, quantity_sold, sales_amount)
            VALUES (%s, %s, %s, %s, %s)
        """, (customer_key, product_key, date_key, qty, amount))


# ---------------------------
# MAIN
# ---------------------------
def main():
    oltp_conn = get_connection(OLTP_DB)
    dw_conn = get_connection(DW_DB)

    oltp_cur = oltp_conn.cursor()
    dw_cur = dw_conn.cursor()

    try:
        load_dim_customer(oltp_cur, dw_cur)
        load_dim_product(oltp_cur, dw_cur)
        load_dim_date(oltp_cur, dw_cur)
        load_fact_sales(oltp_cur, dw_cur)

        dw_conn.commit()
        logging.info("Data Warehouse ETL completed successfully")

    except Exception as e:
        dw_conn.rollback()
        logging.error(f"DW ETL failed: {e}")

    finally:
        oltp_cur.close()
        dw_cur.close()
        oltp_conn.close()
        dw_conn.close()


if __name__ == "__main__":
    main()
