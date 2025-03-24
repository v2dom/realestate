# Real Estate Data Scraper & Dashboard

This tool is created to scrape real estate listings and visualize trends. This was created with the help of DeepSeek, as this served as an introduction to web scraping. DeepSeek explained key topics, helped me overcome anti-scraping mechanisms, and aided the implementation of my ideas into code. AI drastically improved my productivity and allowed me to turn an idea into a fully operational prototype in about one workday's time.

## tech stack

### front

streamlit (interactive UI)

html & css (basic styling)

### back

python

playwright (web scraping)

pandas (data processing)

matplotlib & plotly (data visualization)

sqlite (storing scraped data)

## features

- scrapes real estate listing data from Zillow.

- cleans and structures the data for analysis.

- displays visualizations of market trends (price distribution, average prices over time, etc.).

- allows users to filter and explore specific data points interactively.

## how to run

clone the repository

install dependencies: ```pip install -r requirements.txt```

run the scraper: ```python scraper.py```

start the Streamlit dashboard: ```streamlit run app.py```

## coming soon

- implement API-based data fetching for real-time updates.

- add machine learning models for price predictions.

