import pandas as pd

from utils import scrape_category

BASE_URL = "https://books.toscrape.com/catalogue/category/books/"
CATEGORIES = {
    "travel": "travel_2/index.html",
    "mystery": "mystery_3/index.html",
    "historical-fiction": "historical-fiction_4/index.html",
    "classics": "classics_6/index.html",
}

def scrape_all_categories(categories: dict, base_url: str) -> pd.DataFrame:
    """Scrape all defined categories and return DataFrame."""
    all_books = []
    for cat, url in categories.items():
        books = scrape_category(cat, url, base_url)
        all_books.extend(books)

    return pd.DataFrame(all_books)

def scrape_books_main():
    """Scrape all books from all categories."""
    df = scrape_all_categories(CATEGORIES, BASE_URL)
    print(f"Scraped {len(df)} books.")

    # Save outputs
    df.to_csv("data/books.csv", index=False)
    df.to_json("data/books.json", orient="records", indent=2, force_ascii=False)
    print("Data saved to data/books.csv and data/books.json")

if __name__ == "__main__":
    print("Scraping books...")
    scrape_books_main()