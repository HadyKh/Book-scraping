import re
import pandas as pd
from pathlib import Path

class DataLoader:
    """Load and preprocess scraped book data."""

    def __init__(self, data_path: str | Path):
        self.data_path = Path(data_path)
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")

        if self.data_path.suffix == ".csv":
            self.df = pd.read_csv(self.data_path)
        elif self.data_path.suffix == ".json":
            self.df = pd.read_json(self.data_path)
        else:
            raise ValueError("Unsupported file type. Use CSV or JSON.")

        # Apply preprocessing
        self.clean_data()
    
    def get_dataframe(self) -> pd.DataFrame:
        """Return the cleaned dataframe."""
        return self.df

    @staticmethod
    def parse_price(price) -> float:
        """Convert '£51.77' or 'Â£45.17' → 51.77"""
        if pd.isna(price):
            return None
        clean = re.sub(r"[^0-9.]", "", str(price))
        try:
            return float(clean)
        except ValueError:
            return None
    
    @staticmethod
    def parse_availability(availability: str) -> tuple[str, int]:
        """
        Convert availability string to (status, stock_count).
        e.g., 'In stock (22 available)' → ('In stock', 22)
        """
        if not isinstance(availability, str):
            return ("Unknown", 0)

        status = "In stock" if "In stock" in availability else "Out of stock"
        match = re.search(r"(\d+)", availability)
        stock_count = int(match.group(1)) if match else 0
        return status, stock_count
    
    @staticmethod
    def clean_description(desc: str) -> str:
        """Remove excessive whitespace/HTML artifacts from description."""
        if not isinstance(desc, str):
            return ""
        return re.sub(r"\s+", " ", desc).strip()
    
    @staticmethod
    def normalize_rating(rating) -> int | None:
        """Ensure rating is integer 1–5 or None."""
        try:
            val = int(rating)
            if 1 <= val <= 5:
                return val
        except (ValueError, TypeError):
            return None
        return None
    
    def clean_data(self):
        """Apply normalization to dataframe."""
        self.df["price"] = self.df["price"].apply(self.parse_price)

        availability_data = self.df["availability"].apply(self.parse_availability)
        self.df["availability_status"] = availability_data.apply(lambda x: x[0])
        
        self.df["description"] = self.df["description"].apply(self.clean_description)
        self.df["rating"] = self.df["rating"].apply(self.normalize_rating)

if __name__ == "__main__":
    raw_file = Path("data/books.csv")  # default input
    if not raw_file.exists():
        raise FileNotFoundError("❌ No raw data found. Run the scraper first.")
    
    print("🔄 Loading and cleaning data...")
    loader = DataLoader(raw_file)
    df = loader.get_dataframe()

    cleaned_csv = Path("data/books_clean.csv")
    cleaned_json = Path("data/books_clean.json")

    df.to_csv(cleaned_csv, index=False)
    df.to_json(cleaned_json, orient="records", indent=2, force_ascii=False)

    print(f"✅ Cleaned data saved to {cleaned_csv} and {cleaned_json}")
    print("\n📊 Preview:")
    print(df.head(3))