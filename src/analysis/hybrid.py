import pandas as pd
from pathlib import Path

class HybridAnalysis:
    """Answer hybrid categorical + numerical questions about book dataset."""

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
        
    # Q1 Which category has the highest average price of books? 
    def highest_avg_price_category(self) -> dict:
        averages = self.df.groupby("category")["price"].mean().round(2)
        if averages.empty:
            return {
                "question": "Which category has the highest average price of books?",
                "answer": None,
                "justification": "No data available."
            }
        highest_cat = averages.idxmax()
        highest_val = float(averages.max())
        return {
            "question": "Which category has the highest average price of books?",
            "answer": {"category": highest_cat, "average_price": highest_val},
            "justification": f"{highest_cat} has the highest average price at £{highest_val:.2f}."
        }
    
    # Q2 Which categories have more than 50% of their books priced above £30?
    def categories_majority_over_30(self) -> dict:
        results = {}
        for cat, group in self.df.groupby("category"):
            total = len(group)
            if total == 0:
                continue
            over_30 = len(group[group["price"] > 30])
            ratio = over_30 / total
            if ratio > 0.5:
                results[cat] = round(ratio * 100, 1)

        return {
            "question": "Which categories have more than 50% of their books priced above £30?",
            "answer": results if results else None,
            "justification": (
                f"Categories with >50% of books above £30: {results}"
                if results else "No categories meet this criterion."
            )
        }
    
    # Q3 Compare the average description length (in words) across the four categories. 
    def avg_description_length(self) -> dict:
        self.df["desc_length"] = self.df["description"].fillna("").apply(
            lambda d: len(d.split())
        )
        averages = self.df.groupby("category")["desc_length"].mean().round(2).to_dict()
        return {
            "question": "Compare the average description length (in words) across the categories.",
            "answer": averages,
            "justification": f"Computed average word counts of descriptions for {len(self.df)} books."
        }
    
    # Q4 Which category has the highest percentage of books marked as "Out of stock"? 
    def highest_out_of_stock_percentage(self) -> dict:
        results = {}
        for cat, group in self.df.groupby("category"):
            total = len(group)
            if total == 0:
                continue
            out_stock = len(group[group["availability"] == "Out of stock"])
            pct = (out_stock / total) * 100
            results[cat] = round(pct, 1)

        if not results:
            return {
                "question": "Which category has the highest percentage of books marked as 'Out of stock'?",
                "answer": None,
                "justification": "No data available."
            }

        highest_cat = max(results, key=results.get)
        return {
            "question": "Which category has the highest percentage of books marked as 'Out of stock'?",
            "answer": {"category": highest_cat, "percentage": results[highest_cat]},
            "justification": f"{highest_cat} has {results[highest_cat]}% of its books out of stock."
        }

if __name__ == "__main__":
    analyzer = HybridAnalysis()

    results = [
        analyzer.highest_avg_price_category(),
        analyzer.categories_majority_over_30(),
        analyzer.avg_description_length(),
        analyzer.highest_out_of_stock_percentage(),
    ]

    for res in results:
        print(f"\nQ: {res['question']}")
        print(f"➡️  Answer: {res['answer']}")
        print(f"📌 Justification: {res['justification']}")
