import pandas as pd
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import logging
import re
from collections import defaultdict

# -------------------- CONFIG --------------------

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "asima",
    "database": "fleximart"
}

DATA_PATH = "../data/"

CUSTOMERS_CSV = DATA_PATH + "customers_raw.csv"
PRODUCTS_CSV = DATA_PATH + "products_raw.csv"
SALES_CSV = DATA_PATH + "sales_raw.csv"

# -------------------- LOGGING --------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------- GLOBAL METRICS --------------------

metrics = defaultdict(int)

# -------------------- HELPERS --------------------

def parse_date(value):
    for fmt in ("%d-%m-%Y", "%Y/%m/%d", "%Y-%m-%d"):
        try:
            return datetime.strptime(str(value), fmt).date()
        except ValueError:
            continue
    return None


def standardize_phone(phone):
    if pd.isna(phone):
        return None
    digits = re.sub(r"\D", "", str(phone))
    if len(digits) == 10:
        return f"+91-{digits}"
    return None


# -------------------- DB CONNECTION --------------------

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# -------------------- CUSTOMERS ETL --------------------

def clean_customers(df):
    metrics["customers_read"] = len(df)

    df = df.dropna(
    subset=["email", "first_name", "last_name", "registration_date"]
    ).copy()
    metrics["customers_dropped_missing"] = metrics["customers_read"] - len(df)

    df["email"] = df["email"].str.lower()
    before = len(df)
    df = df.drop_duplicates(subset=["email"])
    metrics["customers_duplicates"] = before - len(df)

    df["phone"] = df["phone"].apply(standardize_phone)
    df["registration_date"] = df["registration_date"].apply(parse_date)
    df = df.dropna(subset=["registration_date"])

    return df


def load_customers(df, conn):
    cursor = conn.cursor()
    inserted = 0

    for _, row in df.iterrows():
        try:
            cursor.execute(
                """
                INSERT INTO customers (first_name, last_name, email, phone, city, registration_date)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    row["first_name"],
                    row["last_name"],
                    row["email"],
                    row["phone"],
                    row.get("city"),
                    row["registration_date"]
                )
            )
            inserted += 1
        except Error:
            pass  # duplicate email (idempotency)

    conn.commit()
    metrics["customers_loaded"] = inserted


# -------------------- PRODUCTS ETL --------------------

def clean_products(df):
    metrics["products_read"] = len(df)

    df = df.dropna(
    subset=["product_name", "category", "price"]
    ).copy()
    df["category"] = df["category"].str.strip().str.lower().str.title()
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    df = df[(df["price"] > 0) & (df["price"] <= 100000)]
    df["stock_quantity"] = df["stock_quantity"].fillna(0).astype(int)

    before = len(df)
    df = df.drop_duplicates(subset=["product_name", "category"])
    metrics["products_duplicates"] = before - len(df)

    return df


def load_products(df, conn):
    cursor = conn.cursor()
    inserted = 0

    for _, row in df.iterrows():
        try:
            cursor.execute(
                """
                INSERT INTO products (product_name, category, price, stock_quantity)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    row["product_name"],
                    row["category"],
                    row["price"],
                    row["stock_quantity"]
                )
            )
            inserted += 1
        except Error:
            pass

    conn.commit()
    metrics["products_loaded"] = inserted


# -------------------- SALES ETL --------------------

def load_sales(df, conn):
    cursor = conn.cursor()

    cursor.execute("SELECT customer_id, email FROM customers")
    customer_map = {email: cid for cid, email in cursor.fetchall()}

    cursor.execute("SELECT product_id, product_name, category, price FROM products")
    product_map = {(name, cat): (pid, price) for pid, name, cat, price in cursor.fetchall()}

    metrics["sales_read"] = len(df)

    df["order_date"] = df["order_date"].apply(parse_date)
    df = df.dropna(subset=["order_date"])

    grouped = df.groupby(["customer_email", "order_date"])

    orders_created = 0
    order_items_created = 0

    for (email, order_date), group in grouped:
        if email not in customer_map:
            metrics["sales_invalid_customer"] += len(group)
            continue

        customer_id = customer_map[email]
        total_amount = 0
        items = []

        for _, row in group.iterrows():
            key = (row["product_name"], row["category"].strip().title())
            if key not in product_map:
                metrics["sales_invalid_product"] += 1
                continue

            product_id, unit_price = product_map[key]
            qty = int(row["quantity"])
            if qty < 1:
                continue

            subtotal = qty * unit_price
            total_amount += subtotal
            items.append((product_id, qty, unit_price, subtotal))

        if not items:
            continue

        try:
            cursor.execute(
                """
                INSERT INTO orders (customer_id, order_date, total_amount)
                VALUES (%s, %s, %s)
                """,
                (customer_id, order_date, total_amount)
            )
            order_id = cursor.lastrowid
            orders_created += 1

            for item in items:
                cursor.execute(
                    """
                    INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (order_id, *item)
                )
                order_items_created += 1

            conn.commit()

        except Error:
            conn.rollback()

    metrics["orders_created"] = orders_created
    metrics["order_items_created"] = order_items_created


# -------------------- REPORT --------------------

def write_report():
    with open("data_quality_report.txt", "w") as f:
        for k, v in metrics.items():
            f.write(f"{k}: {v}\n")


# -------------------- MAIN --------------------

def main():
    try:
        conn = get_connection()

        customers = pd.read_csv(CUSTOMERS_CSV)
        products = pd.read_csv(PRODUCTS_CSV)
        sales = pd.read_csv(SALES_CSV)

        customers_clean = clean_customers(customers)
        load_customers(customers_clean, conn)

        products_clean = clean_products(products)
        load_products(products_clean, conn)

        load_sales(sales, conn)

        write_report()

        logging.info("ETL Pipeline completed successfully")

    except Exception as e:
        logging.error(f"ETL Failed: {e}")

    finally:
        if conn.is_connected():
            conn.close()


if __name__ == "__main__":
    main()
