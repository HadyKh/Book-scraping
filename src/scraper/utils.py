import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_rating(star_class: str) -> int:
    """Convert star rating class to integer."""
    mapping = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5,
    }
    for k, v in mapping.items():
        if k in star_class:
            return v
    return None

def scrape_category(category_name: str, category_url: str, base_url: str) -> list[dict]:
    """Scrape all books from a given category."""
    books = []
    url = urljoin(base_url, category_url)

    while url:
        print(f"Scraping: {url}")
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("article.product_pod")

        for article in articles:
            title = article.h3.a["title"] # Get title

            # Get price
            price_text = article.select_one(".price_color").text.strip()
            clean_price = re.sub(r"[^0-9.]", "", price_text)
            price = float(clean_price.replace("£", ""))

            # Get availability
            availability_text = article.select_one(".availability").text.strip()
            availability = (
                "In stock" if "In stock" in availability_text else "Out of stock"
            )

            # Get rating
            rating = get_rating(article.get("class", [])) or get_rating(
                article.select_one("p.star-rating")["class"]
            )

            # Follow link to get description and stock count
            book_url = urljoin(url, article.h3.a["href"])
            description, availability_raw, stock_count = scrape_book_detail(book_url)

            books.append(
                {
                    "title": title,
                    "category": category_name,
                    "price": price,
                    "availability": availability,
                    "stock_count": stock_count, 
                    "rating": rating,
                    "description": description,
                    "url": book_url,
                }
            )

        # Check for "next" page
        next_button = soup.select_one("li.next > a")
        if next_button:
            next_href = next_button["href"]
            url = urljoin(url, next_href)
        else:
            url = None

        time.sleep(1)

    return books

def scrape_book_detail(book_url: str) -> tuple[str, int, str]:
    """Scrape description and availability (with numeric count) from detail page."""
    response = requests.get(book_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Description
    desc_elem = soup.select_one("#product_description ~ p")
    description = desc_elem.get_text(strip=True) if desc_elem else ""

    # Availability is in the product info table
    availability_raw = ""
    stock_count = 0
    rows = soup.select("table.table.table-striped tr")
    for row in rows:
        header = row.find("th")
        if header and header.get_text(strip=True) == "Availability":
            availability_raw = row.find("td").get_text(strip=True)
            # Normalize whitespace
            availability_raw = re.sub(r"\s+", " ", availability_raw)
            # Extract digits
            match = re.search(r"(\d+)", availability_raw)
            stock_count = int(match.group(1)) if match else 0
            break

    return description, availability_raw, stock_count

# Getting just description (Updated with the function above 'scrape_book_detail')
def scrape_book_description(book_url: str) -> str:
    """Scrape the book description from detail page."""
    response = requests.get(book_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    desc_elem = soup.select_one("#product_description ~ p")

    return desc_elem.text.strip() if desc_elem else ""

