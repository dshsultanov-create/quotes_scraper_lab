from scraper.config import BASE_URL
from scraper.fetch import fetch_page
from scraper.parse import (
    parse_quotes_from_page,
    parse_next_page_url,
    parse_author_page,
)
from scraper.repository import (
    save_quotes,
    get_authors_without_details,
    save_author_details,
)


def scrape_first_page_and_save() -> dict:
    html = fetch_page(BASE_URL)

    quotes = parse_quotes_from_page(
        html,
        page_number=1,
    )

    inserted_count = save_quotes(quotes)

    return {
        "pages_processed": 1,
        "quotes_found": len(quotes),
        "quotes_inserted": inserted_count,
    }


def scrape_all_pages_and_save() -> dict:
    current_url = BASE_URL
    page_number = 1

    total_pages_processed = 0
    total_quotes_found = 0
    total_quotes_inserted = 0

    while current_url:
        html = fetch_page(current_url)

        quotes = parse_quotes_from_page(
            html,
            page_number=page_number,
        )

        inserted_count = save_quotes(quotes)

        total_pages_processed += 1
        total_quotes_found += len(quotes)
        total_quotes_inserted += inserted_count

        current_url = parse_next_page_url(
            html,
            current_url,
        )

        page_number += 1

    return {
        "pages_processed": total_pages_processed,
        "quotes_found": total_quotes_found,
        "quotes_inserted": total_quotes_inserted,
    }


def enrich_authors() -> dict:
    authors = get_authors_without_details()

    total_authors = len(authors)
    enriched_count = 0

    for author in authors:
        author_url = author["author_about_url"]

        html = fetch_page(author_url)
        details = parse_author_page(html)

        save_author_details(
            author_url,
            details,
        )

        enriched_count += 1

    return {
        "authors_found": total_authors,
        "authors_enriched": enriched_count,
    }