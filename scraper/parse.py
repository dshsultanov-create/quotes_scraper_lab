from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scraper.config import BASE_URL


def parse_quotes_from_page(html: str, page_number: int = 1) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")

    quote_blocks = soup.select("div.quote")

    quotes = []

    for block in quote_blocks:
        text_tag = block.select_one("span.text")
        author_tag = block.select_one("small.author")
        about_tag = block.select_one("a[href*='/author/']")
        tag_elements = block.select("div.tags a.tag")

        quote_text = text_tag.get_text(strip=True) if text_tag else ""
        author_name = author_tag.get_text(strip=True) if author_tag else ""

        about_href = about_tag.get("href", "") if about_tag else ""
        author_about_url = urljoin(BASE_URL, about_href) if about_href else ""

        tags = [tag.get_text(strip=True) for tag in tag_elements]

        quotes.append(
            {
                "quote_text": quote_text,
                "author_name": author_name,
                "author_about_url": author_about_url,
                "tags": tags,
                "page_number": page_number,
            }
        )

    return quotes
def parse_next_page_url(html: str, current_url: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")

    next_link = soup.select_one("li.next a")

    if not next_link:
        return None

    href = next_link.get("href", "").strip()

    if not href:
        return None

    return urljoin(current_url, href)

def parse_author_page(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    born_date_tag = soup.select_one(".author-born-date")
    born_location_tag = soup.select_one(".author-born-location")
    description_tag = soup.select_one(".author-description")

    born_date = born_date_tag.get_text(strip=True) if born_date_tag else ""
    born_location = (
        born_location_tag.get_text(strip=True)
        if born_location_tag
        else ""
        
    )
    description = (
        " ".join(description_tag.get_text(" ", strip=True).split())
        if description_tag
        else ""
    )

    return {
        "born_date": born_date,
        "born_location": born_location,
        "description": description,
    }