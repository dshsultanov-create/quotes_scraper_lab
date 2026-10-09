from scraper.parse import (
    parse_quotes_from_page,
    parse_next_page_url,
    parse_author_page,
)

def test_parse_author_page():
    html = """
    <html>
        <body>
            <span class="author-born-date">
                March 14, 1879
            </span>

            <span class="author-born-location">
                in Ulm, Germany
            </span>

            <div class="author-description">
                Albert Einstein was a theoretical physicist.
                He developed the theory of relativity.
            </div>
        </body>
    </html>
    """

    author = parse_author_page(html)

    assert author["born_date"] == "March 14, 1879"
    assert author["born_location"] == "in Ulm, Germany"

    assert (
        author["description"]
        == (
            "Albert Einstein was a theoretical physicist. "
            "He developed the theory of relativity."
        )
    )

def test_parse_next_page_url():
    html = """
    <html>
        <body>
            <ul class="pager">
                <li class="next">
                    <a href="/page/2/">Next</a>
                </li>
            </ul>
        </body>
    </html>
    """

    next_url = parse_next_page_url(
        html,
        "https://quotes.toscrape.com/",
    )

    assert next_url == "https://quotes.toscrape.com/page/2/"

def test_parse_quotes_from_page():
    html = """
    <html>
        <body>
            <div class="quote">
                <span class="text">
                    “Test quote”
                </span>

                <span>
                    by
                    <small class="author">
                        Test Author
                    </small>

                    <a href="/author/Test-Author">
                        (about)
                    </a>
                </span>

                <div class="tags">
                    <a class="tag">test</a>
                    <a class="tag">python</a>
                </div>
            </div>
        </body>
    </html>
    """

    quotes = parse_quotes_from_page(
        html,
        page_number=3,
    )

    assert len(quotes) == 1

    quote = quotes[0]

    assert quote["quote_text"] == "“Test quote”"
    assert quote["author_name"] == "Test Author"

    assert (
        quote["author_about_url"]
        == "https://quotes.toscrape.com/author/Test-Author"
    )

    assert quote["tags"] == [
        "test",
        "python",
    ]

    assert quote["page_number"] == 3

def test_parse_next_page_url_when_no_next_page():
    html = """
    <html>
        <body>
            <ul class="pager">
                <li class="previous">
                    <a href="/page/9/">Previous</a>
                </li>
            </ul>
        </body>
    </html>
    """

    next_url = parse_next_page_url(
        html,
        "https://quotes.toscrape.com/page/10/",
    )

    assert next_url is None
    