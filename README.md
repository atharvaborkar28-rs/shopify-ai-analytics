Shopify AI Analytics Assistant

A FastAPI-based AI analytics assistant that connects with the Shopify Admin REST API to answer natural-language business questions related to orders, revenue, products, and customers.

1. Project Overview

This project demonstrates how an AI-style backend service can fetch and analyze Shopify store data using REST APIs and return meaningful insights such as order counts, revenue trends, top-selling products, and repeat customers. The system is implemented using FastAPI and tested using Postman.

2. Setup Instructions
Prerequisites

Python 3.10+

Shopify development store

Shopify Admin API access token

Git

Steps

Clone the repository

git clone https://github.com/atharvaborkar28-rs/shopify-ai-analytics.git
cd shopify-ai-analytics


Create & activate virtual environment (optional but recommended)

python -m venv venv
venv\Scripts\activate   # Windows


Install dependencies

pip install -r requirements.txt


Run the FastAPI server

uvicorn main:app --reload


Open API documentation

http://127.0.0.1:8000/docs

3. Architecture Explanation

FastAPI Backend: Handles API requests and response formatting

Rule-based Intent Layer: Detects intent from user questions

Shopify Admin REST API: Fetches orders, revenue, products, and customer data

Postman: Used for API testing and validation

User → POST /ask → Intent Detection → Shopify REST API → Analytics Logic → Response

4. Agent Flow Description

User sends a POST request to /ask

Backend identifies intent from the question text

Shopify Admin API is queried accordingly

Data is processed (filters, aggregation, counts)

Structured JSON response is returned to the user

5. Sample API Requests & Responses
Example 1: Orders in last 30 days

Request

POST /ask
{
  "store": "2mbtgf-0d",
  "question": "How many orders in last 30 days?"
}


Response

{
  "intent": "sales",
  "answer": "There are 8 orders in the last 30 days."
}

Example 2: Total Revenue

Request

{
  "store": "2mbtgf-0d",
  "question": "What is the total revenue in last 30 days?"
}


Response

{
  "intent": "sales",
  "answer": "Total revenue in the last 30 days is ₹3414.70"
}


6. Screenshots & Evidence

The screenshots folder contains visual proof of working functionality:

Shopify Admin

shopify_app.jpg – Shopify app & admin access

Shopify orders.jpg – Orders visible in Shopify dashboard

Postman API Results

Postman orders.jpg, Postman orders 2.jpg, Postman Orders 1.jpg – Orders API

Postman Revenue.jpg – Revenue calculation

Postman Product sold.jpg – Top-selling product

postman Loyal customer.jpg, Postman more than once.jpg – Repeat customers

Postman admin.jpg – Admin API access

Postman Fallback.jpg – Unknown question handling

7. Repository Structure
ai-service/
│── main.py
│── requirements.txt
│── README.md
│── .gitignore
│── screenshots/
│   ├── Postman orders.jpg
│   ├── Postman Revenue.jpg
│   ├── postman Loyal customer.jpg
│   ├── shopify_app.jpg
│   └── Shopify orders.jpg

