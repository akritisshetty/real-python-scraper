"""PostgreSQL persistence for scraped articles."""
import os

import psycopg2
from psycopg2.extras import execute_values

SCHEMA = """
CREATE TABLE IF NOT EXISTS articles (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    description TEXT,
    published_at DATE,
    categories TEXT[] NOT NULL DEFAULT '{}',
    scraped_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""

UPSERT = """
INSERT INTO articles (url, title, description, published_at, categories)
VALUES %s
ON CONFLICT (url) DO UPDATE SET
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    published_at = EXCLUDED.published_at,
    categories = EXCLUDED.categories,
    scraped_at = now();
"""


def connect():
    return psycopg2.connect(os.environ["DATABASE_URL"])


def init_db(conn):
    with conn.cursor() as cur:
        cur.execute(SCHEMA)
    conn.commit()


def save_rows(conn, rows):
    values = [(r["url"], r["title"], r["description"], r["published_at"], r["categories"]) for r in rows]
    with conn.cursor() as cur:
        execute_values(cur, UPSERT, values)
    conn.commit()