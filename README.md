# HTTP QUERY Method API — FastAPI + SQLite

A hands-on implementation demonstrating the HTTP `QUERY` method alongside the traditional `GET` method using **Python, FastAPI, and SQLite**.

This project explores two approaches to retrieving resources with filtering criteria:

- **GET:** Pass filtering criteria through URL query parameters.
- **QUERY:** Send structured query criteria in the request content.

Both endpoints operate on the same SQLite database and share the same filtering logic, making their behavior easy to compare.

> **Project goal:** Understand and experiment with the HTTP QUERY method through a small, reproducible REST API.

---

## Table of Contents

- [Overview](#overview)
- [Why HTTP QUERY?](#why-http-query)
- [GET vs QUERY](#get-vs-query)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Running the Application](#running-the-application)
- [API Reference](#api-reference)
- [Example Requests](#example-requests)
- [Expected Response](#expected-response)
- [Testing with Postman](#testing-with-postman)
- [How It Works Internally](#how-it-works-internally)
- [Security and Design Considerations](#security-and-design-considerations)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [References](#references)
- [Author](#author)

---

## Overview

HTTP APIs commonly use `GET` requests to retrieve resources. Filtering criteria are typically represented through URL query parameters.

For example:

```http
GET /products?category=electronics&min_price=500&max_price=5000
```

This approach works well for many use cases. However, as query requirements become more complex, URLs can become long and difficult to manage.

The HTTP `QUERY` method provides another approach by allowing clients to send query instructions in the request content.

For example:

```http
QUERY /products
Content-Type: application/json

{
  "category": "electronics",
  "min_price": 500,
  "max_price": 5000
}
```

This project implements both approaches using the same underlying SQLite database.

### What this project demonstrates

- Implementing `GET` and `QUERY` endpoints in FastAPI.
- Passing filtering criteria through URL parameters and JSON request content.
- Using SQLite for persistent local storage.
- Reusing business logic across multiple HTTP endpoints.
- Validating incoming query parameters and request bodies with Pydantic.
- Testing a custom HTTP method using Postman and curl.
- Inspecting API operations through OpenAPI documentation.

---

## Why HTTP QUERY?

The HTTP `QUERY` method is specified in [RFC 10008 — The HTTP QUERY Method](https://www.rfc-editor.org/rfc/rfc10008.html).

It defines a standardized HTTP method for requests that carry query instructions in their content. QUERY is defined as a **safe and idempotent** method.

This makes it useful to explore when an application needs to express structured queries without placing all criteria in the URL.

For example, a product search might include several filters:

- Product category
- Minimum and maximum price
- Text search
- Result limit

With QUERY, these criteria can be represented in a JSON object rather than encoded as URL parameters.

### Why not use GET for everything?

GET remains an appropriate choice for ordinary resource retrieval and simple filtering. QUERY provides an additional option for query-oriented use cases.

This project focuses on comparing how the two methods represent the same filtering criteria.

**Important:** QUERY does not automatically make a request faster, more secure, or more efficient than GET. This project demonstrates differences in request representation and does not benchmark performance.

---

## GET vs QUERY

| Feature | GET | QUERY |
|---|---|---|
| HTTP method | `GET` | `QUERY` |
| Endpoint in this project | `/products` | `/products` |
| Filtering criteria | URL query parameters | Request content |
| Request body for filters | Not used in this implementation | Yes |
| Request format in this demo | URL parameters | JSON |
| Response format | JSON | JSON |
| Database | SQLite | SQLite |
| Filtering implementation | Shared function | Shared function |
| Safe method | Yes | Yes, as defined by RFC 10008 |
| Idempotent method | Yes | Yes, as defined by RFC 10008 |
| Primary purpose in this demo | Conventional resource retrieval | Structured query instructions |

The two endpoints intentionally share the same URL path. The HTTP method determines which operation handles the request.

### GET example

```http
GET /products?category=electronics&min_price=500&max_price=5000&limit=10
```

### QUERY example

```http
QUERY /products
Content-Type: application/json

{
  "category": "electronics",
  "min_price": 500,
  "max_price": 5000,
  "limit": 10
}
```

For equivalent filters, both requests should return the same matching products.

This project demonstrates a difference in request representation, not a performance improvement.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application programming language |
| FastAPI | HTTP API framework |
| Uvicorn | ASGI application server |
| SQLite | Local relational database |
| Pydantic | Request validation and data modeling |
| Postman | Manual API testing |
| curl | Command-line HTTP testing |
| Git | Version control |
| GitHub | Source code hosting |

SQLite is available through Python's standard-library `sqlite3` module. A separate database server is not required.

---

## Architecture

The application follows a simple request-processing flow:

```text
                   API Client
                (Postman / curl)
                       |
                       v
                FastAPI Application
                       |
               +-------+-------+
               |               |
               v               v
          GET /products   QUERY /products
               |               |
               v               v
          Parse URL       Validate JSON
          parameters      request body
               |               |
               +-------+-------+
                       |
                       v
                 ProductFilters
                       |
                       v
                find_products()
                       |
                       v
                   SQLite DB
                       |
                       v
                  JSON Response
```

The key design decision is the shared `find_products()` function. Both endpoints use the same filtering and database access logic, reducing duplication and keeping their behavior consistent.

---

## Project Structure

```text
http-query-method-api/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── products.db       # Generated locally; not committed
```

### File descriptions

- `main.py` — FastAPI application, SQLite initialization, sample data, request validation, and both endpoints.
- `requirements.txt` — Python dependencies.
- `README.md` — Project documentation and usage instructions.
- `.gitignore` — Excludes virtual environments, generated databases, and other local artifacts.
- `products.db` — Local SQLite database generated when the application starts.

The database is created automatically. A fresh installation does not require a pre-existing database file.

---

## Prerequisites

Before starting, install:

- Python 3.11 or a compatible newer version.
- Git.
- Postman, if you want to test requests through a graphical client.

Verify your installation:

```bash
python --version
git --version
```

You do not need MySQL, PostgreSQL, Docker, or a paid database service for this demonstration.

---

## Installation and Setup

### 1. Clone the repository


```bash
git clone https://github.com/SatanJordon/http-query-method-api.git
cd http-query-method-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows Command Prompt**

```bat
.venv\Scripts\activate.bat
```

**Linux or macOS**

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

The `requirements.txt` file should contain:

```text
fastapi
uvicorn
```

Pydantic is installed as a dependency of FastAPI and is used for request validation.

For reproducible builds, consider pinning dependency versions after testing the application with those versions.

---

## Running the Application

Start the development server:

```bash
uvicorn main:app --reload
```

The application should be available at:

| Resource | URL |
|---|---|
| API root | http://127.0.0.1:8000/ |
| Interactive Swagger UI | http://127.0.0.1:8000/docs |
| OpenAPI schema | http://127.0.0.1:8000/openapi.json |
| ReDoc | http://127.0.0.1:8000/redoc |

The application initializes the SQLite database during startup and inserts the sample products if the table is empty.

Keep the server running while testing requests.

**Note:** Swagger UI may not display or allow execution of QUERY operations in every version. Use a compatible HTTP client such as Postman or curl to test the actual request.

---

## API Reference

### 1. GET `/products`

Retrieves products using URL query parameters.

**Method:** `GET`

**Path:** `/products`

#### Supported parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `category` | String | No | Exact category match |
| `min_price` | Number | No | Minimum price, inclusive |
| `max_price` | Number | No | Maximum price, inclusive |
| `search` | String | No | Case-insensitive substring search on the product name |
| `limit` | Integer | No | Maximum number of returned records; defaults to 10, range 1–100 |

#### Example request

```http
GET /products?category=electronics&min_price=500&max_price=5000&limit=10
```

#### Example with text search

```http
GET /products?search=keyboard&limit=10
```

### 2. QUERY `/products`

Retrieves products using structured query criteria in the request content.

**Method:** `QUERY`

**Path:** `/products`

**Content-Type:** `application/json`

#### Request schema

| Field | Type | Required | Validation |
|---|---|---|---|
| `category` | String or null | No | Exact category match |
| `min_price` | Number or null | No | Must be greater than or equal to zero |
| `max_price` | Number or null | No | Must be greater than or equal to zero |
| `search` | String or null | No | Product-name substring search |
| `limit` | Integer | No | Defaults to 10; range 1–100 |

#### Example request

```http
QUERY /products
Content-Type: application/json

{
  "category": "electronics",
  "min_price": 500,
  "max_price": 5000,
  "limit": 10
}
```

The request content is validated using the `ProductFilters` Pydantic model.

The `search` field is optional. If provided, the application also filters products by a substring of their names.

**Note:** The current implementation performs an exact category match and a substring search on the product name. It does not implement advanced full-text search.

---

## Example Requests

### Example 1: Retrieve electronics priced between 500 and 5000

**GET**

```bash
curl "http://127.0.0.1:8000/products?category=electronics&min_price=500&max_price=5000&limit=10"
```

**QUERY**

```bash
curl -X QUERY "http://127.0.0.1:8000/products" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "electronics",
    "min_price": 500,
    "max_price": 5000,
    "limit": 10
  }'
```

The QUERY command uses POSIX shell quoting and works in Linux and macOS terminals and many Git Bash environments. In Windows PowerShell, use Postman or `curl.exe` with appropriately escaped JSON.

### Example 2: Search for a keyboard

**GET**

```http
GET /products?search=keyboard
```

**QUERY**

```http
QUERY /products
Content-Type: application/json

{
  "search": "keyboard"
}
```

Both requests use the same matching logic.

### Example 3: Retrieve furniture within a price range

**GET**

```http
GET /products?category=furniture&min_price=1000&max_price=5000
```

**QUERY**

```http
QUERY /products
Content-Type: application/json

{
  "category": "furniture",
  "min_price": 1000,
  "max_price": 5000
}
```

For equivalent filters and an unchanged database, both requests should return the same matching records.

---

## Expected Response

For the electronics request with a minimum price of 500 and maximum price of 5000, the seeded database returns four matching products.

```json
{
  "count": 4,
  "filters": {
    "category": "electronics",
    "min_price": 500.0,
    "max_price": 5000.0,
    "search": null,
    "limit": 10
  },
  "products": [
    {
      "id": 1,
      "name": "Mechanical Keyboard",
      "category": "electronics",
      "price": 2500.0
    },
    {
      "id": 2,
      "name": "Wireless Mouse",
      "category": "electronics",
      "price": 1200.0
    },
    {
      "id": 3,
      "name": "USB-C Hub",
      "category": "electronics",
      "price": 3200.0
    },
    {
      "id": 6,
      "name": "Webcam",
      "category": "electronics",
      "price": 4000.0
    }
  ]
}
```

The response includes:

- `count` — Number of product records returned.
- `filters` — The normalized filtering criteria applied.
- `products` — The matching product records.

**Important:** In this implementation, `count` reflects the number of returned records, not necessarily the total number of matches in the database when a result limit is applied.

The exact response depends on the sample data and the filters supplied in the request.

---

## Testing with Postman

Postman is useful for comparing both methods because you can inspect the request method, parameters or body, response status, and returned JSON.

### Test GET

1. Create a new HTTP request.
2. Select `GET`.
3. Enter:

   ```text
   http://127.0.0.1:8000/products
   ```

4. Open the **Params** tab.
5. Add the following parameters:

   | Key | Value |
   |---|---|
   | `category` | `electronics` |
   | `min_price` | `500` |
   | `max_price` | `5000` |
   | `limit` | `10` |

6. Click **Send**.

Expected result: `200 OK`, with four matching products.

### Test QUERY

1. Create another HTTP request.
2. Select `QUERY` from the method dropdown, or enter the custom method if supported by your Postman version.
3. Enter:

   ```text
   http://127.0.0.1:8000/products
   ```

4. Under **Headers**, set:

   ```text
   Content-Type: application/json
   ```

5. Open **Body → raw → JSON**.
6. Paste:

   ```json
   {
     "category": "electronics",
     "min_price": 500,
     "max_price": 5000,
     "limit": 10
   }
   ```

7. Click **Send**.

Expected result: `200 OK`, with the same four products.

### What to compare

- Request method.
- Where the filtering criteria are represented.
- Response status.
- Returned product IDs and values.
- Response structure.

For a meaningful comparison, use equivalent filters and ensure the database contents have not changed between requests.

---

## How It Works Internally

### 1. Database initialization

At startup, the application creates the `products` table if it does not exist.

If the table contains no records, six sample products are inserted.

SQLite provides persistent local storage through Python's built-in `sqlite3` module.

### 2. Request validation

The `ProductFilters` Pydantic model defines the allowed query fields and their constraints.

For example:

- `limit` must be between 1 and 100.
- Price values cannot be negative.
- Optional fields may be omitted.

FastAPI validates incoming request data and returns a validation error when the input violates the declared constraints.

### 3. Shared filtering logic

Both endpoints convert their inputs into a `ProductFilters` object and call:

```python
find_products(filters)
```

This function builds the SQL query from a fixed set of permitted filtering conditions.

It does not accept arbitrary SQL from the client.

### 4. Parameterized SQL

User-provided values are passed to SQLite as query parameters rather than interpolated directly into the SQL statement.

For example:

```python
conditions.append("category = ?")
parameters.append(filters.category)
```

This helps protect against SQL injection through the filter values.

### 5. Consistent responses

Both endpoints use the same database query function and response format.

This keeps the comparison focused on the HTTP request method and the representation of query criteria.

---

## Security and Design Considerations

This is a learning project, not a production-ready API.

The implementation demonstrates several useful practices:

- **Parameterized SQL:** User values are passed separately from SQL syntax.
- **Input validation:** Pydantic constrains supported fields and values.
- **Bounded result size:** The maximum requested result limit is 100.
- **Shared business logic:** Both methods use the same query implementation.
- **Restricted filtering:** Clients cannot supply arbitrary SQL expressions through the API.

### Important security considerations

QUERY allows query criteria to be sent in request content, but this does not guarantee confidentiality.

Request content may still be captured by application logs, reverse proxies, monitoring systems, or other infrastructure. Sensitive data should not be included in query requests unless the application has appropriate protections in place.

Additional work would be required before production deployment, including:

- Authentication and authorization.
- HTTPS for traffic in transit.
- Rate limiting and abuse prevention.
- Appropriate request-size limits.
- Structured logging with sensitive-data redaction.
- Consistent exception handling.
- Operational monitoring and alerting.
- Dependency updates and security reviews.

If the project is extended with more filters, the SQL builder should continue to use a fixed allowlist of permitted fields and parameterized values.

---

## Limitations

- This is a small demonstration with six seeded products.
- The application does not benchmark performance between GET and QUERY.
- QUERY support in HTTP clients, reverse proxies, gateways, and API documentation tools may vary.
- SQLite is suitable for this local demonstration but may not be the right database for every production workload.
- The current search implementation uses SQL `LIKE` and does not provide advanced full-text search.
- The database is persistent, so manual modifications remain until the data is changed or the database is reset.
- The initial dependency list does not pin exact versions.
- The project focuses on the core request-handling example rather than implementing every feature described by the QUERY specification.

---

## Future Improvements

Possible next steps for this project include:

- Add automated tests to verify that equivalent GET and QUERY requests return equivalent results.
- Advertise supported query formats using the `Accept-Query` response header.
- Add pagination and sorting.
- Introduce additional filtering criteria.
- Add structured logging and improved error handling.
- Pin dependency versions for reproducible installations.
- Test behavior through different HTTP clients, reverse proxies, and API gateways.
- Explore how OpenAPI documentation tools represent QUERY operations.

These improvements would make the project more robust while keeping its original educational purpose.

---

## References

- [RFC 10008 — The HTTP QUERY Method](https://www.rfc-editor.org/rfc/rfc10008.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python `sqlite3` Documentation](https://docs.python.org/3/library/sqlite3.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Postman Documentation](https://learning.postman.com/)

---

## Author

**Sayan Chakraborty**  
Backend Java Developer | Python & REST API Enthusiast

This project was built as a hands-on exploration of HTTP methods, API design, and structured query handling using Python, FastAPI, and SQLite.

**LinkedIn:** [Connect with me](https://www.linkedin.com/in/sayan-chakraborty-332604149/)

If you find this project useful, feel free to ⭐ the repository, experiment with the implementation, and share your feedback.

---

*Built for learning, experimentation, and discussion about evolving HTTP API design.*