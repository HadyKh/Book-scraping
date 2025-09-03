import pandas as pd
from pathlib import Path


class CategoricalAnalysis:
    """Answer categorical yes/no questions about book dataset."""

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
        
    # Q1 Are there any books in the "Travel" category that are marked as "Out of stock"?
    def travel_out_of_stock(self) -> dict:
        subset = self.df[(self.df["category"] == "travel") &
                        (self.df["availability"] == "Out of stock")]
        count = len(subset)
        return {
            "question": "Are there any books in the 'Travel' category that are out of stock?",
            "answer": "Yes" if count > 0 else "No",
            "justification": (f"{count} travel books are out of stock. Examples: {subset['title'].head(3).tolist()}"
                            if count > 0 else "No travel books are out of stock.")
        }
    
    # Q2 Does the "Mystery" category contain books with a 5-star rating?
    def mystery_five_star(self) -> dict:
        subset = self.df[(self.df["category"] == "mystery") & (self.df["rating"] == 5)]
        count = len(subset)
        return {
            "question": "Does the 'Mystery' category contain books with a 5-star rating?",
            "answer": "Yes" if count > 0 else "No",
            "justification": (
                f"{count} mystery books with 5★ rating. Examples: {subset['title'].head(3).tolist()}"
                if count > 0 else "No 5★ books found in mystery category."
            )
        }
    
    # Q3 Are there books in the "Classics" category priced below £10? 
    def classics_under_10(self) -> dict:
        subset = self.df[(self.df["category"] == "classics") & (self.df["price"] < 10)]
        count = len(subset)
        return {
            "question": "Are there books in the 'Classics' category priced below £10?",
            "answer": "Yes" if count > 0 else "No",
            "justification": (
                f"{count} classics under £10. Examples: {subset[['title','price']].head(3).to_dict(orient='records')}" 
                if count > 0 else "No classics found under £10."
            )
        }
    
    # Q4 Are more than 50% of books in the "Mystery" category priced above £20? 
    def mystery_over_20_majority(self) -> dict:
        subset = self.df[self.df["category"] == "mystery"]
        total = len(subset)
        if total == 0:
            return {
                "question": "Are more than 50% of books in the 'Mystery' category priced above £20?",
                "answer": "No",
                "justification": "No mystery books found in dataset."
            }

        above_20 = subset[subset["price"] > 20]
        ratio = len(above_20) / total
        return {
            "question": "Are more than 50% of books in the 'Mystery' category priced above £20?",
            "answer": "Yes" if ratio > 0.5 else "No",
            "justification": f"{len(above_20)}/{total} mystery books ({ratio:.0%}) are priced above £20."
        }

if __name__ == "__main__":
    analyzer = CategoricalAnalysis()

    results = [
        analyzer.travel_out_of_stock(),
        analyzer.mystery_five_star(),
        analyzer.classics_under_10(),
        analyzer.mystery_over_20_majority(),
    ]

    for res in results:
        print(f"\nQ: {res['question']}")
        print(f"➡️  Answer: {res['answer']}")
        print(f"📌 Justification: {res['justification']}")