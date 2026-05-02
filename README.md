# 🚗 My Mechanic Shop API

## 📌 Project Overview

The **My Mechanic Shop API** is a RESTful backend application built with Flask that simulates a real-world mechanic shop system. It allows users to manage customers, mechanics, service tickets, and inventory.

The system supports:

* Customer registration and authentication (JWT-based)
* Creating and managing service tickets
* Assigning mechanics to service tickets
* Adding/removing parts from tickets
* Managing inventory and pricing

This project demonstrates API design, database relationships, authentication, and testing using modern backend practices.

---

## 🛠️ Tech Stack

* **Backend:** Flask
* **Database:** SQLite (SQLAlchemy ORM)
* **Validation:** Marshmallow
* **Authentication:** JWT (custom token system)
* **Rate Limiting:** Flask-Limiter
* **Caching:** Flask-Caching
* **API Docs:** Swagger UI
* **Testing:** Python unittest

---

## ⚙️ How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/CodingWithMBJ/my-mechanic-shop.git
cd my-mechanic-shop
```

### 2. Create & Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python run.py
```

The API will be available at:

```
http://127.0.0.1:5000
```

---

## 📄 API Documentation (Swagger)

Swagger UI is available at:

```
http://127.0.0.1:5000/api/docs
```

Use this interface to:

* Test endpoints
* View request/response schemas
* Authenticate using bearer tokens

---

## 🔐 Authentication

Most protected routes require a token.

### Steps:

1. Login via:

```
POST /customers/login
```

2. Copy the token from the response

3. Add it to headers:

```
Authorization: Bearer <your_token>
```

---

## 📡 API Endpoints

### 👤 Customers

* `POST /customers/` → Create customer
* `POST /customers/login` → Login
* `GET /customers/` → Get all customers (paginated)
* `GET /customers/{id}` → Get single customer
* `PUT /customers/{id}` → Update customer (auth required)
* `DELETE /customers/` → Delete logged-in customer

---

### 🔧 Mechanics

* `POST /mechanics/`
* `GET /mechanics/`
* `GET /mechanics/{id}`
* `PUT /mechanics/{id}`
* `DELETE /mechanics/{id}`

---

### 🧾 Service Tickets

* `POST /service-tickets/`
* `GET /service-tickets/` (auth required)
* `GET /service-tickets/my-tickets` (auth required)
* `PUT /service-tickets/{id}/edit` (auth required)

#### Mechanics Assignment

* `PUT /service-tickets/{id}/assign-mechanic/{mechanic_id}`
* `PUT /service-tickets/{id}/remove-mechanic/{mechanic_id}`

#### Parts Management

* `PUT /service-tickets/{id}/add-part/{part_id}` (auth required)

---

### 📦 Inventory

* `POST /inventory/`
* `GET /inventory/`
* `GET /inventory/{id}`
* `PUT /inventory/{id}`
* `DELETE /inventory/{id}`

---

## 🧪 Running Tests

To run all tests:

```bash
python -m unittest discover tests
```

Tests include:

* Customer authentication and CRUD
* Service ticket creation and relationships
* Mechanic assignment/removal
* Inventory interactions

---

## 🧱 Database Relationships

This project includes advanced relationships:

* **Customer → Service Tickets** (One-to-Many)
* **Service Tickets ↔ Mechanics** (Many-to-Many)
* **Service Tickets ↔ Inventory** (Many-to-Many)

---

## 🚀 Future Improvements

* Role-based authentication (admin vs customer)
* Payment integration
* Frontend dashboard (React)
* Deployment to cloud (Render / AWS)

---

## 👨‍💻 Author

Mohamed Jalloh

---

## 📬 Notes

This project was built as part of a backend development assignment demonstrating API design, testing, and system architecture.
