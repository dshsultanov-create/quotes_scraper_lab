from scraper import workflow


def test_run_full_workflow(monkeypatch):
    def fake_scrape_all_pages_and_save():
        return {
            "pages_processed": 10,
            "quotes_found": 100,
            "quotes_inserted": 5,
        }

    def fake_enrich_authors():
        return {
            "authors_found": 3,
            "authors_enriched": 3,
        }

    def fake_export_all_to_google_sheets():
        return {
            "quotes_exported": 100,
            "authors_exported": 50,
        }

    monkeypatch.setattr(
        workflow,
        "scrape_all_pages_and_save",
        fake_scrape_all_pages_and_save,
    )

    monkeypatch.setattr(
        workflow,
        "enrich_authors",
        fake_enrich_authors,
    )

    monkeypatch.setattr(
        workflow,
        "export_all_to_google_sheets",
        fake_export_all_to_google_sheets,
    )

    result = workflow.run_full_workflow()

    assert result == {
        "pages_processed": 10,
        "quotes_found": 100,
        "quotes_inserted": 5,
        "authors_enriched": 3,
        "quotes_exported": 100,
        "authors_exported": 50,
    }