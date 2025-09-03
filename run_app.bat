@echo off
setlocal

REM ---- Step 1: create venv if not exists ----
if not exist "env" (
    echo Creating virtual environment...
    python -m venv env
)

REM ---- Step 2: activate venv ----
call env\Scripts\activate.bat

REM ---- Step 3: install requirements ----
if exist requirements.txt (
    echo Installing requirements...
    pip install -r requirements.txt
)

REM ---- Step 4: check if data/books.csv exists ----
if not exist "data\books.csv" (
    echo books.csv not found. Running scraper...
    python src\scraper\scraper.py
)
else (
    echo books.csv found. Skipping scraper...
)

REM ---- Step 5: data preprocessing ----
echo data preprocessing is not needed. skipping preprocessing...
REM -- python src\preprocessing\data_loader.py


REM ---- Step 4: run Streamlit ----
echo Starting Streamlit app...
streamlit run src/app.py

endlocal
