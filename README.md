# Book Data Extractor & QA Engine

This project scrapes book data from [Books to Scrape](https://books.toscrape.com),
extracts categorical and numerical insights, and provides an interactive UI
(Streamlit) for question answering.

## features
- **Web Scraping**: Extracts book data including title, category, price, rating, availability, and stock count
- **Data Analysis**: Predefined questions with intelligent answers and justifications
- **Interactive UI**: Streamlit-based interface with dropdown question selection
- **Search Functionality**: Quick search by book title
- **Category Browser**: Interactive category bubbles to explore books by genre

## Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Automatic Installation & Initialization (Windows)
**Simply double-click on `run_app.bat`** and the script will automatically:
1. Create a virtual environment (if it doesn't exist)
2. Install all required dependencies
3. Scrape fresh book data from the website (if books.csv doesn't exist)
4. Preprocess the data (Skipped)
5. Launch the Streamlit application in your default browser

*Note: The first run may take a few minutes to set up everything.*

### Manual Installation & Initialization
```bash
# Create virtual environment
python -m venv env
.\env\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Books scrapping
python src\scraper\scraper.py

# Books preprocessing
# Please note this step is no longer needed automatically handled during scrapping
python src\preprocessing\data_loader.py

# UI Initialization
streamlit run src/app.py
```

## 📝 Notes
- The application requires an internet connection to scrape fresh data
- Data is cached for better performance on subsequent runs
- All scraped data is saved to src/data/books_data.csv

## 🧩 Dependencies
- **streamlit** - Interactive web application
- **pandas** - Data manipulation and analysis
- **requests** & beautifulsoup4 - Web scraping
- **numpy** - Numerical computations