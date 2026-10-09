from scraper.service import (
    scrape_all_pages_and_save,
    enrich_authors,
)
from scraper.sheets_sync import export_all_to_google_sheets


def run_full_workflow() -> dict:
    scrape_result = scrape_all_pages_and_save()

    enrich_result = enrich_authors()

    export_result = export_all_to_google_sheets()

    return {
        "pages_processed": scrape_result["pages_processed"],
        "quotes_found": scrape_result["quotes_found"],
        "quotes_inserted": scrape_result["quotes_inserted"],
        "authors_enriched": enrich_result["authors_enriched"],
        "quotes_exported": export_result["quotes_exported"],
        "authors_exported": export_result["authors_exported"],
    }