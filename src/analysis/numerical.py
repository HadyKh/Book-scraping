import pandas as pd
from pathlib import Path

class NumericalAnalysis:
    """Answer numerical questions about book dataset."""

    def __init__(self, data_path: str | Path = "data/books.csv"):
        self.data_path = Path(data_path)

        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")

        if self.data_path.suffix == ".csv":
            self.df = pd.read_csv(self.data_path)
        elif self.data_path.suffix == ".json":
            self.df = pd.read_json(self.data_path)
        else:
            raise ValueError("Unsupported file type. Use CSV or JSON.")
    
    # Q1 What is the average price of books across each category? 
    def average_price_per_category(self) -> dict:
        averages = self.df.groupby("category")["price"].mean().round(2).to_dict()
        return {
            "question": "What is the average price of books across each category?",
            "answer": averages,
            "justification": f"Calculated mean price per category from {len(self.df)} books."
        }
    
    # Q2 What is the price range (minimum and maximum) for books in the "Historical Fiction" category? 
    def historical_fiction_price_range(self) -> dict:
        subset = self.df[self.df["category"] == "historical-fiction"]
        if subset.empty:
            return {
                "question": "What is the price range for books in 'Historical Fiction'?",
                "answer": None,
                "justification": "No Historical Fiction books found."
            }
        min_price, max_price = subset["price"].min(), subset["price"].max()
        return {
            "question": "What is the price range (min and max) for books in 'Historical Fiction'?",
            "answer": {"min": str(round(min_price, 2)), "max": str(round(max_price, 2))},
            "justification": f"From {len(subset)} books, min={min_price:.2f}, max={max_price:.2f}"
        }
    
    # Q3 How many books are available in stock across the four categories? 
    def total_in_stock(self) -> dict:
        subset = self.df[self.df["availability"] == "In stock"]
        total_stock = subset["stock_count"].sum()
        return {
            "question": "How many books are available in stock across the four categories?",
            "answer": int(total_stock),
            "justification": f"Summed stock counts of {len(subset)} in-stock books."
        }
    
    # Q4 What is the total value (sum of prices) of all books in the "Travel" category? 
    def total_value_travel(self) -> dict:
        subset = self.df[self.df["category"] == "travel"]
        total_value = (subset["price"] * subset["stock_count"]).sum()
        return {
            "question": "What is the total value (sum of prices × stock) of all books in the 'Travel' category?",
            "answer": round(float(total_value), 2),
            "justification": f"Calculated by summing {len(subset)} travel books with stock counts."
        }
    
if __name__ == "__main__":
    analyzer = NumericalAnalysis()

    results = [
        analyzer.average_price_per_category(),
        analyzer.historical_fiction_price_range(),
        analyzer.total_in_stock(),
        analyzer.total_value_travel(),
    ]

    for res in results:
        print(f"\nQ: {res['question']}")
        print(f"➡️  Answer: {res['answer']}")
        print(f"📌 Justification: {res['justification']}")