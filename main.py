
import sqlite3
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Body, FastAPI, Query
from pydantic import BaseModel, Field

DATABASE = "products.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL
            )
        """)

        count = connection.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

        if count == 0:
            connection.executemany(
                """
                INSERT INTO products (name, category, price)
                VALUES (?, ?, ?)
                """,
                [
                    ("Mechanical Keyboard", "electronics", 2500),
                    ("Wireless Mouse", "electronics", 1200),
                    ("USB-C Hub", "electronics", 3200),
                    ("Office Chair", "furniture", 4500),
                    ("Standing Desk", "furniture", 12000),
                    ("Webcam", "electronics", 4000),
                ],
            )


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="HTTP QUERY vs GET",
    description="Compare GET query parameters with HTTP QUERY request bodies.",
    lifespan=lifespan,
)


class ProductFilters(BaseModel):
    category: str | None = None
    min_price: float | None = Field(default=None, ge=0)
    max_price: float | None = Field(default=None, ge=0)
    search: str | None = None
    limit: int = Field(default=10, ge=1, le=100)


def find_products(filters: ProductFilters):
    conditions = []
    parameters = []

    if filters.category:
        conditions.append("category = ?")
        parameters.append(filters.category)

    if filters.min_price is not None:
        conditions.append("price >= ?")
        parameters.append(filters.min_price)

    if filters.max_price is not None:
        conditions.append("price <= ?")
        parameters.append(filters.max_price)

    if filters.search:
        conditions.append("name LIKE ?")
        parameters.append(f"%{filters.search}%")

    sql = "SELECT id, name, category, price FROM products"

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    sql += " ORDER BY id LIMIT ?"
    parameters.append(filters.limit)

    with get_connection() as connection:
        rows = connection.execute(sql, parameters).fetchall()

    return {
        "count": len(rows),
        "filters": filters.model_dump(),
        "products": [dict(row) for row in rows],
    }


@app.get("/products")
def get_products(
    category: str | None = None,
    min_price: Annotated[float | None, Query(ge=0)] = None,
    max_price: Annotated[float | None, Query(ge=0)] = None,
    search: str | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    filters = ProductFilters(
        category=category,
        min_price=min_price,
        max_price=max_price,
        search=search,
        limit=limit,
    )
    return find_products(filters)


@app.api_route("/products", methods=["QUERY"])
def query_products(
    filters: Annotated[ProductFilters, Body()]
):
    return find_products(filters)


@app.get("/")
def root():
    return {
        "message": "Compare GET and QUERY",
        "get_endpoint": "GET /products",
        "query_endpoint": "QUERY /products",
        "docs": "/docs",
    }


if __name__ == "__main__":
    for route in app.routes:
        print(
            getattr(route, "methods", None),
            getattr(route, "path", None)
        )