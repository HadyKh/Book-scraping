import sys
import pandas as pd
from pathlib import Path

# sys.path.append(str(Path(__file__).resolve().parents[2]))

from .categorical import CategoricalAnalysis
from .numerical import NumericalAnalysis
from .hybrid import HybridAnalysis

class QuestionAnswerer:
    """Unified Q&A Engine that maps questions to analysis functions."""

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
        
        # Initialize analysis modules
        self._initialize_analysis_modules()
        # Map questions to functions
        self.question_mapping()
    
    def get_dataframe(self) -> pd.DataFrame:
        """Return the loaded dataframe."""
        return self.df
    
    def get_questions(self):
        return [{"id": qid, "description": desc} for qid, (desc, _) in self.questions.items()]
        
    def _initialize_analysis_modules(self):
        self.categorical = CategoricalAnalysis(self.data_path)
        self.numerical = NumericalAnalysis(self.data_path)
        self.hybrid = HybridAnalysis(self.data_path)
    
    def question_mapping(self):
         self.questions = {
            # Categorical
            "cat_travel_out": (
                "Are there any books in the 'Travel' category that are out of stock?",
                self.categorical.travel_out_of_stock,
            ),
            "cat_mystery_5star": (
                "Does the 'Mystery' category contain books with a 5-star rating?",
                self.categorical.mystery_five_star,
            ),
            "cat_classics_under10": (
                "Are there books in the 'Classics' category priced below £10?",
                self.categorical.classics_under_10,
            ),
            "cat_mystery_majority20": (
                "Are more than 50% of books in the 'Mystery' category priced above £20?",
                self.categorical.mystery_over_20_majority,
            ),
            # Numerical
            "num_avg_price_cat": (
                "What is the average price of books across each category?",
                self.numerical.average_price_per_category,
            ),
            "num_histfic_range": (
                "What is the price range (min and max) for books in 'Historical Fiction'?",
                self.numerical.historical_fiction_price_range,
            ),
            "num_total_in_stock": (
                "How many books are available in stock across the four categories?",
                self.numerical.total_in_stock,
            ),
            "num_total_value_travel": (
                "What is the total value of books in the 'Travel' category?",
                self.numerical.total_value_travel,
            ),
            # Hybrid
            "hyb_highest_avg_price": (
                "Which category has the highest average price of books?",
                self.hybrid.highest_avg_price_category,
            ),
            "hyb_majority_over30": (
                "Which categories have more than 50% of their books priced above £30?",
                self.hybrid.categories_majority_over_30,
            ),
            "hyb_desc_length": (
                "Compare the average description length across categories.",
                self.hybrid.avg_description_length,
            ),
            "hyb_highest_out_stock": (
                "Which category has the highest percentage of books marked as 'Out of stock'?",
                self.hybrid.highest_out_of_stock_percentage,
            ),
        }
    
    def answer_question(self, question_key: str) -> dict:
        if question_key not in self.questions:
            raise ValueError(f"Unknown question id: {question_key}")
        _, func = self.questions[question_key]
        return func()
    
if __name__ == "__main__":
    qa = QuestionAnswerer()

    print("📋 Available Questions:")
    for q in qa.get_questions():
        print(f" - {q['id']}: {q['description']}")

    print("\n🔎 Sample Answers:")
    for qid in ["cat_travel_out", "num_avg_price_cat", "hyb_highest_avg_price"]:
        res = qa.answer_question(qid)
        print(f"\nQ: {res['question']}")
        print(f"➡️  Answer: {res['answer']}")
        print(f"📌 Justification: {res['justification']}")