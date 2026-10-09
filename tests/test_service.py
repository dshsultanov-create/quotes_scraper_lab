from scraper import service


def test_scrape_first_page_and_save(monkeypatch):
    fake_html = """
    <html>
        <body>
            <div class="quote">
                <span class="text">
                    “Mocked test quote”
                </span>

                <span>
                    by
                    <small class="author">
                        Mock Author
                    </small>

                    <a href="/author/Mock-Author">
                        (about)
                    </a>
                </span>

                <div class="tags">
                    <a class="tag">testing</a>
                    <a class="tag">mocking</a>
                </div>
            </div>
        </body>
    </html>
    """

    def fake_fetch_page(url):
        return fake_html

    def fake_save_quotes(quotes):
        assert len(quotes) == 1

        quote = quotes[0]

        assert quote["quote_text"] == "“Mocked test quote”"
        assert quote["author_name"] == "Mock Author"

        assert (
            quote["author_about_url"]
            == "https://quotes.toscrape.com/author/Mock-Author"
        )

        assert quote["tags"] == [
            "testing",
            "mocking",
        ]

        assert quote["page_number"] == 1

        return 1

    monkeypatch.setattr(
        service,
        "fetch_page",
        fake_fetch_page,
    )

    monkeypatch.setattr(
        service,
        "save_quotes",
        fake_save_quotes,
    )

    result = service.scrape_first_page_and_save()

    assert result == {
        "pages_processed": 1,
        "quotes_found": 1,
        "quotes_inserted": 1,
    }


def test_scrape_all_pages_and_save(monkeypatch):
    page_1_html = """
    <html>
        <body>
            <div class="quote">
                <span class="text">
                    “Quote from page one”
                </span>

                <span>
                    by
                    <small class="author">
                        Author One
                    </small>

                    <a href="/author/Author-One">
                        (about)
                    </a>
                </span>

                <div class="tags">
                    <a class="tag">page-one</a>
                </div>
            </div>

            <ul class="pager">
                <li class="next">
                    <a href="/page/2/">Next</a>
                </li>
            </ul>
        </body>
    </html>
    """

    page_2_html = """
    <html>
        <body>
            <div class="quote">
                <span class="text">
                    “Quote from page two”
                </span>

                <span>
                    by
                    <small class="author">
                        Author Two
                    </small>

                    <a href="/author/Author-Two">
                        (about)
                    </a>
                </span>

                <div class="tags">
                    <a class="tag">page-two</a>
                </div>
            </div>
        </body>
    </html>
    """

    requested_urls = []
    saved_quotes = []

    def fake_fetch_page(url):
        requested_urls.append(url)

        if url == "https://quotes.toscrape.com/":
            return page_1_html

        if url == "https://quotes.toscrape.com/page/2/":
            return page_2_html

        raise AssertionError(
            f"Unexpected URL requested: {url}"
        )

    def fake_save_quotes(quotes):
        saved_quotes.extend(quotes)

        return len(quotes)

    monkeypatch.setattr(
        service,
        "fetch_page",
        fake_fetch_page,
    )

    monkeypatch.setattr(
        service,
        "save_quotes",
        fake_save_quotes,
    )

    result = service.scrape_all_pages_and_save()

    assert result == {
        "pages_processed": 2,
        "quotes_found": 2,
        "quotes_inserted": 2,
    }

    assert requested_urls == [
        "https://quotes.toscrape.com/",
        "https://quotes.toscrape.com/page/2/",
    ]

    assert len(saved_quotes) == 2

    assert saved_quotes[0]["quote_text"] == "“Quote from page one”"
    assert saved_quotes[0]["author_name"] == "Author One"
    assert saved_quotes[0]["page_number"] == 1

    assert saved_quotes[1]["quote_text"] == "“Quote from page two”"
    assert saved_quotes[1]["author_name"] == "Author Two"
    assert saved_quotes[1]["page_number"] == 2


def test_enrich_authors(monkeypatch):
    fake_authors = [
        {
            "id": 1,
            "author_name": "Author One",
            "author_about_url": (
                "https://quotes.toscrape.com/author/Author-One"
            ),
        },
        {
            "id": 2,
            "author_name": "Author Two",
            "author_about_url": (
                "https://quotes.toscrape.com/author/Author-Two"
            ),
        },
    ]

    fake_author_pages = {
        "https://quotes.toscrape.com/author/Author-One": (
            "HTML FOR AUTHOR ONE"
        ),
        "https://quotes.toscrape.com/author/Author-Two": (
            "HTML FOR AUTHOR TWO"
        ),
    }

    fake_parsed_details = {
        "HTML FOR AUTHOR ONE": {
            "born_date": "January 1, 1900",
            "born_location": "in City One",
            "description": "Biography of Author One.",
        },
        "HTML FOR AUTHOR TWO": {
            "born_date": "February 2, 1950",
            "born_location": "in City Two",
            "description": "Biography of Author Two.",
        },
    }

    requested_urls = []
    saved_details = []

    def fake_get_authors_without_details():
        return fake_authors

    def fake_fetch_page(url):
        requested_urls.append(url)

        return fake_author_pages[url]

    def fake_parse_author_page(html):
        return fake_parsed_details[html]

    def fake_save_author_details(
        author_about_url,
        details,
    ):
        saved_details.append(
            {
                "author_about_url": author_about_url,
                "details": details,
            }
        )

    monkeypatch.setattr(
        service,
        "get_authors_without_details",
        fake_get_authors_without_details,
    )

    monkeypatch.setattr(
        service,
        "fetch_page",
        fake_fetch_page,
    )

    monkeypatch.setattr(
        service,
        "parse_author_page",
        fake_parse_author_page,
    )

    monkeypatch.setattr(
        service,
        "save_author_details",
        fake_save_author_details,
    )

    result = service.enrich_authors()

    assert result == {
        "authors_found": 2,
        "authors_enriched": 2,
    }

    assert requested_urls == [
        "https://quotes.toscrape.com/author/Author-One",
        "https://quotes.toscrape.com/author/Author-Two",
    ]

    assert len(saved_details) == 2

    assert saved_details[0] == {
        "author_about_url": (
            "https://quotes.toscrape.com/author/Author-One"
        ),
        "details": {
            "born_date": "January 1, 1900",
            "born_location": "in City One",
            "description": "Biography of Author One.",
        },
    }

    assert saved_details[1] == {
        "author_about_url": (
            "https://quotes.toscrape.com/author/Author-Two"
        ),
        "details": {
            "born_date": "February 2, 1950",
            "born_location": "in City Two",
            "description": "Biography of Author Two.",
        },
    }