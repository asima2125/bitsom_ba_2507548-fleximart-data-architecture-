# Database Schema Documentation – FlexiMart (Part 1)

## 1. Entity–Relationship Description

### ENTITY: customers

**Purpose:**  
Stores master information about customers registered on the FlexiMart platform.

**Attributes:**

- `customer_id` (PK): Surrogate primary key uniquely identifying each customer
- `first_name`: Customer’s first name
- `last_name`: Customer’s last name
- `email`: Unique email address used for customer identification
- `phone`: Contact number in standardized format
- `city`: City of residence
- `registration_date`: Date when the customer registered

**Relationships:**

- One customer can place **many orders**
- Relationship: `customers (1) → orders (M)`

---

### ENTITY: products

**Purpose:**  
Stores product catalog information available for sale.

**Attributes:**

- `product_id` (PK): Surrogate primary key
- `product_name`: Name of the product
- `category`: Product category (e.g., Electronics, Furniture)
- `price`: Unit selling price
- `stock_quantity`: Available inventory count

**Relationships:**

- One product can appear in **many order items**
- Relationship: `products (1) → order_items (M)`

---

### ENTITY: orders

**Purpose:**  
Stores order-level transactional information for each purchase.

**Attributes:**

- `order_id` (PK): Unique identifier for each order
- `customer_id` (FK): References `customers.customer_id`
- `order_date`: Date when the order was placed
- `total_amount`: Total monetary value of the order
- `status`: Order status (default: Pending)

**Relationships:**

- Each order belongs to **one customer**
- Each order contains **many order items**

---

### ENTITY: order_items

**Purpose:**  
Stores line-item level details of products within an order.

**Attributes:**

- `order_item_id` (PK): Surrogate primary key
- `order_id` (FK): References `orders.order_id`
- `product_id` (FK): References `products.product_id`
- `quantity`: Number of units ordered
- `unit_price`: Price per unit at the time of purchase
- `subtotal`: Calculated as quantity × unit_price

**Relationships:**

- Each order item belongs to **one order**
- Each order item references **one product**

---

## 2. Normalization Explanation (3NF)

The FlexiMart database schema is designed in **Third Normal Form (3NF)** to ensure data integrity, reduce redundancy, and avoid update anomalies. In this design, each table represents a single entity, and all non-key attributes are fully functionally dependent on the primary key.

In the `customers` table, all attributes such as name, email, phone, and city depend solely on `customer_id`, and no attribute depends on another non-key attribute. Similarly, the `products` table stores only product-specific attributes that depend on `product_id`. There are no transitive dependencies present.

The `orders` table separates order-level information from product details. Attributes like `order_date` and `total_amount` depend only on `order_id`, while customer details are referenced using a foreign key, avoiding duplication of customer data. The `order_items` table further decomposes order details by storing product-level quantities and pricing, ensuring that multiple products within an order are handled without redundancy.

This design eliminates **update anomalies** (e.g., changing a product price in one place), **insert anomalies** (e.g., adding products without orders), and **delete anomalies** (e.g., deleting an order does not remove customer data). Overall, the schema ensures consistency, scalability, and efficient transactional processing.

---

## 3. Sample Data Representation

### customers

| customer_id | first_name | last_name | email                | city   |
| ----------- | ---------- | --------- | -------------------- | ------ |
| 1           | John       | Doe       | john.doe@gmail.com   | Mumbai |
| 2           | Jane       | Smith     | jane.smith@gmail.com | Delhi  |

---

### products

| product_id | product_name | category    | price |
| ---------- | ------------ | ----------- | ----- |
| 1          | Laptop Pro   | Electronics | 75000 |
| 2          | Office Chair | Furniture   | 8000  |

---

### orders

| order_id | customer_id | order_date | total_amount |
| -------- | ----------- | ---------- | ------------ |
| 101      | 1           | 2024-01-15 | 85000        |
| 102      | 2           | 2024-01-16 | 45000        |

---

### order_items

| order_item_id | order_id | product_id | quantity | subtotal |
| ------------- | -------- | ---------- | -------- | -------- |
| 1             | 101      | 1          | 1        | 75000    |
| 2             | 101      | 2          | 1        | 10000    |

---

## 4. Summary

The FlexiMart database schema follows a clean, normalized relational design suitable for transactional systems. By separating customers, products, orders, and order items into distinct entities, the schema ensures data consistency, scalability, and accurate business reporting while adhering strictly to Third Normal Form principles.
