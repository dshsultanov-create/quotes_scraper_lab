import os

import requests
from dotenv import load_dotenv

from scraper.repository import (
    get_all_authors,
    get_all_quotes,
)

load_dotenv()


WEB_APP_URL = os.getenv("SHEETS_WEB_APP_URL")
API_TOKEN = os.getenv("SHEETS_API_TOKEN")


def send_rows(data_type: str, rows: list[dict]) -> dict:
    if not WEB_APP_URL:
        raise ValueError("SHEETS_WEB_APP_URL is not configured.")

    if not API_TOKEN:
        raise ValueError("SHEETS_API_TOKEN is not configured.")

    payload = {
        "token": API_TOKEN,
        "type": data_type,
        "rows": rows,
    }

    response = requests.post(
        WEB_APP_URL,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    result = response.json()

    if not result.get("success"):
        raise RuntimeError(
            result.get(
                "error",
                "Unknown Google Sheets error.",
            )
        )

    return result


def export_quotes() -> dict:
    quotes = get_all_quotes()

    return send_rows(
        "quotes",
        quotes,
    )


def export_authors() -> dict:
    authors = get_all_authors()

    return send_rows(
        "authors",
        authors,
    )


def export_all_to_google_sheets() -> dict:
    quotes_result = export_quotes()
    authors_result = export_authors()

    return {
        "quotes_exported": quotes_result["rows_received"],
        "authors_exported": authors_result["rows_received"],
    }