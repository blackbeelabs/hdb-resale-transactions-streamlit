# HDB Resale Dataset Dashboard

## Introduction
Data visualisation & exploration tool for HDB Resale prices. The public dashboard has 7 years of data, but the full dataset can be found in the `assets` folder.


## Quickstart
Initialise your Python environment. I use `pyenv` / `virtualenv`, and Python `3.11.1
```
pyenv virtualenv 3.11.1 env
pyenv activate env
pip install -r requirements-streamlit.txt
```

Then go to the homepage and run the application
```
cd /path/to/app
streamlit run Home.py
```

Alternatively, visit the URL (on the project properties) to interact with the app.

## Notes:
- `assets/entity-transaction.csv` contains 7 years of data, used in the public dashboard
- `assets/entity-transaction-full.csv` contains the full dataset