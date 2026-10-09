import sqlite3
from datetime import datetime

from scraper.config import DB_PATH


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_name TEXT NOT NULL,
            author_about_url TEXT NOT NULL UNIQUE,
            born_date TEXT,
            born_location TEXT,
            description TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote_text TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            tags TEXT,
            page_number INTEGER,
            scraped_at TEXT NOT NULL,

            UNIQUE(quote_text, author_id),

            FOREIGN KEY(author_id)
                REFERENCES authors(id)
        )
        """
    )

    conn.commit()
    conn.close()


def get_or_create_author(
    cursor,
    author_name: str,
    author_about_url: str,
) -> int:
    cursor.execute(
        """
        INSERT OR IGNORE INTO authors (
            author_name,
            author_about_url
        )
        VALUES (?, ?)
        """,
        (
            author_name,
            author_about_url,
        ),
    )

    cursor.execute(
        """
        SELECT id
        FROM authors
        WHERE author_about_url = ?
        """,
        (author_about_url,),
    )

    row = cursor.fetchone()

    return row["id"]


def save_quotes(quotes: list[dict]) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    inserted_count = 0

    for quote in quotes:
        author_id = get_or_create_author(
            cursor,
            quote["author_name"],
            quote["author_about_url"],
        )

        tags_as_text = ", ".join(quote["tags"])

        cursor.execute(
            """
            INSERT OR IGNORE INTO quotes (
                quote_text,
                author_id,
                tags,
                page_number,
                scraped_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                quote["quote_text"],
                author_id,
                tags_as_text,
                quote["page_number"],
                datetime.now().isoformat(),
            ),
        )

        if cursor.rowcount == 1:
            inserted_count += 1

    conn.commit()
    conn.close()

    return inserted_count


def save_author_details(
    author_about_url: str,
    details: dict,
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE authors
        SET
            born_date = ?,
            born_location = ?,
            description = ?
        WHERE author_about_url = ?
        """,
        (
            details["born_date"],
            details["born_location"],
            details["description"],
            author_about_url,
        ),
    )

    conn.commit()
    conn.close()


def get_authors_without_details() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            author_name,
            author_about_url
        FROM authors
        WHERE born_date IS NULL
        ORDER BY author_name
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_all_authors() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            author_name,
            author_about_url,
            born_date,
            born_location,
            description
        FROM authors
        ORDER BY author_name
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_authors_count() -> int:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM authors")
    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_all_quotes() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            quotes.id,
            quotes.quote_text,
            authors.author_name,
            authors.author_about_url,
            quotes.tags,
            quotes.page_number,
            quotes.scraped_at
        FROM quotes
        JOIN authors
            ON quotes.author_id = authors.id
        ORDER BY quotes.id DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_quotes_count() -> int:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM quotes")
    count = cursor.fetchone()[0]

    conn.close()

    return count