# zomato-food-delivery-analytics-system
End-to-End Food Delivery Analytics Platform using Flask, MySQL, Pandas, ETL, SQL Analytics.
# 🍕 Zomato Food Delivery Analytics System

## 📌 Project Overview

An end-to-end food delivery application inspired by Zomato, built using Python, Flask, MySQL, HTML, CSS, and JavaScript. The project allows users to browse food items, place orders, and store transactional data in a MySQL database. It also includes an ETL pipeline for transforming operational data into analytics-ready datasets.

---

## 🚀 Features

* Food browsing and ordering system
* Customer registration and login
* Shopping cart functionality
* Order management system
* RESTful API built using Flask
* MySQL database integration
* ETL pipeline using Pandas and SQLAlchemy
* SQL analytics and reporting queries

---

## 🛠️ Tech Stack

| Layer           | Technology            |
| --------------- | --------------------- |
| Frontend        | HTML, CSS, JavaScript |
| Backend         | Python, Flask         |
| Database        | MySQL                 |
| ETL             | Pandas, SQLAlchemy    |
| API Testing     | Postman               |
| Version Control | Git, GitHub           |

---

## 📁 Project Structure

```text
zomato-project/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── db.py
│   └── routes.py
│
├── database/
│   └── schema.sql
│
├── etl/
│   └── etl_pipeline.py
│
├── analytics/
│   └── data_analysis.sql
│
└── README.md
```

---

## 📊 Database Design

The project uses a normalized relational database consisting of:

* customers
* orders
* order_items
* foods
* delivery_details

### Relationship Flow

customers → orders → order_items → foods

orders → delivery_details

---

## 🔌 API Endpoints

| Method | Endpoint   | Description           |
| ------ | ---------- | --------------------- |
| GET    | /foods     | Retrieve all foods    |
| GET    | /food/<id> | Retrieve food details |
| POST   | /add-order | Create a new order    |
| GET    | /orders    | View all orders       |
| GET    | /customers | View all customers    |
| POST   | /customer  | Add customer          |
| POST   | /register  | Register user         |
| POST   | /login     | User login            |

---

## 🔄 ETL Pipeline

The ETL pipeline performs:

### Extract

* Reads data from MySQL tables

### Transform

* Handles missing values
* Formats dates
* Creates analytics-ready datasets

### Load

* Loads transformed data into analytics tables
* Generates CSV exports for reporting

---

## 📈 SQL Analytics

The project contains SQL queries for:

* Revenue Analysis
* Customer Analysis
* Top Selling Foods
* Order Trends
* Delivery Performance
* Category-wise Sales
* Customer Spending Patterns
* Monthly Revenue Reports

---

## ▶️ How to Run

### Database Setup

```bash
mysql -u root -p < database/schema.sql
```

### Start Backend

```bash
cd backend
pip install flask flask-cors pymysql sqlalchemy pandas
python app.py
```

### Open Frontend

Open `frontend/index.html` in your browser.

### Run ETL Pipeline

```bash
cd etl
python etl_pipeline.py
```

---

## 🧠 Skills Demonstrated

* SQL Query Writing
* Database Design
* Relational Data Modeling
* REST API Development
* ETL Pipeline Development
* Data Cleaning and Transformation
* Backend Development using Flask
* Git and GitHub Version Control

---

## 📌 Future Enhancements

* Power BI Dashboard Integration
* Advanced Business Analytics
* Customer Recommendation System
* Authentication using JWT
* Cloud Deployment

---

## 👨‍💻 Author

Developed as a Data Engineering and Analytics project to strengthen practical skills in database management, backend development, ETL processes, and analytical SQL.
