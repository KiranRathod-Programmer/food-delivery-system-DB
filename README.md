# 🍴 FoodKart — Food Ordering Application

FoodKart is a **Python-based Food Ordering Application** developed using **Object-Oriented Programming (OOP)** principles and integrated with **PostgreSQL** for persistent data storage.

The project demonstrates how an OOP-based application can be connected to a relational database using a layered **Repository + Service architecture**, while maintaining transaction safety and clean separation of responsibilities.

---

##  Project Overview

FoodKart simulates the core workflow of a food ordering system:

* Customer registration
* Delivery address management
* Food menu management
* Cart management
* Order placement
* Payment processing
* Order status management
* Customer profile viewing
* Order history during the application session
* PostgreSQL database persistence

The project focuses on applying practical **Python OOP, database integration, SQL, transactions, exception handling, and software architecture** concepts in a single application.

---

## 🛠️ Tech Stack

| Technology                  | Purpose                        |
| --------------------------- | ------------------------------ |
| Python                      | Application development        |
| Object-Oriented Programming | Application domain modelling   |
| PostgreSQL                  | Persistent relational database |
| psycopg2                    | Python–PostgreSQL connectivity |
| SQL                         | Database operations            |
| Git & GitHub                | Version control                |

---

##  OOP Concepts Used

The application uses several core OOP concepts.

### Encapsulation

Application data is maintained using private attributes.

Examples:

* `User`
* `Customer`
* `FoodItem`
* `Cart`
* `Order`
* `Payment`

### Inheritance

`Customer` inherits from the `User` class.

```text
User
  │
  └── Customer
```

### Polymorphism

Different payment methods are implemented through specialized payment classes:

```text
Payment
 ├── UPIPayment
 ├── CardPayment
 └── CashPayment
```

Each payment type provides its own payment behaviour through the `pay()` method.

### Abstraction

The base `Payment` class defines the common payment interface while individual payment classes provide the implementation.

---

## 🏗️ Project Architecture

FoodKart follows a layered architecture to separate application responsibilities.

```text
main.py
   │
   │ Application flow
   ▼
Services
   │
   │ Business operations
   ▼
Repositories
   │
   │ SQL / Database operations
   ▼
PostgreSQL
```

### Models

Contains the application's domain objects.

```text
models/
├── user.py
├── customer.py
├── address.py
├── food_item.py
├── cart.py
├── order.py
└── payment.py
```

### Repositories

Responsible for database operations.

```text
database/repositories/
├── customer_repository.py
├── address_repository.py
├── food_repository.py
├── order_repository.py
└── payment_repository.py
```

### Services

Responsible for coordinating application-level operations and transactions.

```text
database/services/
├── customer_service.py
├── food_service.py
└── checkout_service.py
```

---

## 📂 Project Structure

```text
FoodOrderingApp/
│
├── main.py
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── customer.py
│   ├── address.py
│   ├── food_item.py
│   ├── cart.py
│   ├── order.py
│   └── payment.py
│
└── database/
    ├── __init__.py
    ├── connection.py
    ├── test_connection.py
    │
    ├── repositories/
    │   ├── customer_repository.py
    │   ├── address_repository.py
    │   ├── food_repository.py
    │   ├── order_repository.py
    │   └── payment_repository.py
    │
    └── services/
        ├── __init__.py
        ├── customer_service.py
        ├── food_service.py
        ├── checkout_service.py
        └── test_checkout_transaction.py
```

---

## 🗄️ Database Design

The application uses PostgreSQL with six tables.

```text
customers
    │
    │ 1 : 1
    ▼
addresses

customers
    │
    │ 1 : N
    ▼
orders
    │
    │ 1 : N
    ▼
order_items
    │
    │ N : 1
    ▼
food_items

orders
    │
    │ 1 : 1
    ▼
payments
```

### Database Tables

#### `customers`

Stores customer information.

* Customer ID
* Name
* Email
* Phone

#### `addresses`

Stores the delivery address associated with a customer.

* Address ID
* Customer ID
* City
* Pincode
* State

#### `food_items`

Stores available food items.

* Food ID
* Food name
* Price

#### `orders`

Stores placed orders.

* Order ID
* Customer ID
* Total
* Status
* Order date

#### `order_items`

Acts as the bridge between orders and food items.

* Order item ID
* Order ID
* Food item ID
* Quantity
* Price

#### `payments`

Stores payment information associated with an order.

* Payment ID
* Order ID
* Amount
* Payment method
* Payment status
* Payment date

---

## 🔗 Database Relationships

```text
Customer
   │
   ├────────── Address
   │             1 : 1
   │
   └────────── Orders
                 1 : N
                   │
                   ├──────── Order Items ─────── Food Items
                   │              N : 1
                   │
                   └──────── Payment
                                1 : 1
```

The `order_items` table represents the many-to-many relationship between orders and food items.

```text
Order N : N FoodItem

        through

       order_items
```

---

## 🔄 Application Workflow

### 1. Customer Registration

The application collects:

* Name
* Email
* Phone
* City
* Pincode
* State

The customer and address are stored using a single database transaction.

```text
User Input
    │
    │ INSERT customer data
    ▼
customers
    │
    │ RETURNING customer ID
    ▼
customer_id
    │
    │ passed to address creation
    ▼
addresses
```

If an error occurs, the transaction is rolled back.

---

### 2. Food Menu

Food items are stored in PostgreSQL.

```text
food_items
    │
    │ SELECT food items
    ▼
food_repository
    │
    ▼
food_service
    │
    │ creates FoodItem objects
    ▼
main.py
    │
    ▼
Food Menu
```

---

### 3. Cart

The cart is maintained in application memory.

A food item can be added with a quantity. If the same food item is added again, its quantity is increased instead of creating a duplicate cart entry.

Example:

```text
Pizza × 2
Pizza × 3
```

becomes:

```text
Pizza × 5
```

---

### 4. Checkout

Checkout coordinates the complete order transaction.

```text
Cart
 │
 │ calculate total
 ▼
checkout_service
 │
 │ INSERT order
 ▼
orders
 │
 │ INSERT order items
 ▼
order_items
 │
 │ INSERT payment
 ▼
payments
 │
 │ update order status
 ▼
CONFIRMED
```

All database operations are performed within a single transaction.

If any operation fails:

```text
Error
  │
  ▼
ROLLBACK
  │
  ▼
No partial order data remains
```

---

## 💳 Payment Methods

FoodKart supports three payment methods:

```text
Payment
 ├── UPI
 ├── Card
 └── Cash on Delivery
```

For the current implementation:

| Payment Method   | Payment Status |
| ---------------- | -------------- |
| UPI              | SUCCESS        |
| Card             | SUCCESS        |
| Cash on Delivery | PENDING        |

The payment classes demonstrate polymorphic behaviour through the common `pay()` interface.

---

## 🔐 Data Integrity

The PostgreSQL schema uses database constraints to maintain data consistency.

Examples include:

* Primary keys
* Foreign keys
* Unique constraints
* NOT NULL constraints
* CHECK constraints

Examples:

```sql
UNIQUE (order_id, food_item_id)
```

prevents duplicate food entries for the same order.

```sql
CHECK (quantity > 0)
```

ensures that an order item cannot have an invalid quantity.

Foreign keys maintain relationships between customers, orders, food items, and payments.

---

## 🔄 Transaction Management

The project uses explicit PostgreSQL transactions for multi-step operations.

For checkout:

```text
BEGIN
  │
  ├── Create Order
  ├── Create Order Items
  ├── Create Payment
  └── Update Order Status
  │
  ▼
COMMIT
```

If any operation fails:

```text
BEGIN
  │
  ├── Create Order
  ├── Create Order Item
  ├── Error
  │
  ▼
ROLLBACK
```

This prevents partially completed orders from remaining in the database.

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd FoodOrderingApp
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install psycopg2-binary
```

### 4. Create PostgreSQL Database

Create a database named:

```text
food_ordering_db
```

Create the required tables according to the project's database schema.

### 5. Configure Database Connection

Update:

```text
database/connection.py
```

with your PostgreSQL credentials.

Example:

```python
connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="food_ordering_db",
    user="postgres",
    password="YOUR_PASSWORD"
)
```

> For a production application, database credentials should be stored in environment variables rather than directly in source code.

---

## 🍴 Add Food Data

Before running the application, add food items to the `food_items` table.

Example:

```sql
INSERT INTO food_items (name, price)
VALUES
    ('Pizza', 250.00),
    ('Burger', 150.00),
    ('Biryani', 220.00),
    ('Pasta', 180.00),
    ('Sandwich', 100.00);
```

---

## ▶️ Running the Application

Run:

```bash
python main.py
```

The application provides the following menu:

```text
========== MAIN MENU ==========

1. View Food Menu
2. Add Food to Cart
3. View Cart
4. Checkout
5. View Orders
6. View Profile
7. Exit
```

---

## 🧪 Transaction Testing

The project includes a transaction rollback test.

Run:

```bash
python -m database.services.test_checkout_transaction
```

The test verifies that when a checkout transaction fails, the database changes are rolled back instead of leaving incomplete order records.

---

## Learning Objectives

This project was developed to practice and demonstrate:

* Python Object-Oriented Programming
* Encapsulation
* Inheritance
* Polymorphism
* Abstraction
* Class design
* Exception handling
* PostgreSQL
* SQL queries
* Primary and foreign keys
* Database normalization concepts
* Repository pattern
* Service layer
* Transaction management
* Commit and rollback
* Python–PostgreSQL integration
* Data integrity and constraints

---

##  Future Improvements

Possible extensions for the application include:

* Restaurant management
* Admin functionality
* Delivery partner module
* Authentication and authorization
* Persistent cart storage
* Persistent order-history retrieval
* Order cancellation
* Food categories
* Restaurant-wise menus
* Payment gateway integration
* REST API using FastAPI
* Frontend integration
* Environment-based configuration
* Automated unit and integration tests

---

## 👩‍💻 Author

**Kiran Rathod**

B.Tech — Artificial Intelligence & Data Science

---

## 📄 Project Status

**Status:** Completed core OOP + PostgreSQL integration

The current version demonstrates an end-to-end food ordering workflow using Python OOP, PostgreSQL, repository/service architecture, and transaction-safe checkout processing.
