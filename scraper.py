import pandas as pd
import sqlite3
from playwright.sync_api import sync_playwright
import time
import random

def scrape_listings(zip_code, radius):
    URL = f"https://www.zillow.com/homes/{zip_code}_rb/{radius}_miles/"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto(URL)
        
        time.sleep(random.uniform(5, 10))
        
        page_source = page.content()
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(page_source)
        
        try:
            page.wait_for_selector(".StyledPropertyCardDataWrapper-c11n-8-109-3__sc-hfbvv9-0", timeout=60000)
        except Exception as e:
            print(f"Error waiting for listings: {e}")
            browser.close()
            return pd.DataFrame()

        listings = page.query_selector_all(".StyledPropertyCardDataWrapper-c11n-8-109-3__sc-hfbvv9-0")
        if not listings:
            print("No listings found. Check the page source for anti-bot measures.")
            browser.close()
            return pd.DataFrame()
        
        data = []
        for item in listings:
            price_element = item.query_selector(".PropertyCardWrapper__StyledPriceLine-srp-8-109-3__sc-16e8gqd-1")
            price = price_element.inner_text() if price_element else "Price not found"

            address_element = item.query_selector("address")
            address = address_element.inner_text() if address_element else "Address not found"

            details = item.query_selector(".StyledPropertyCardHomeDetailsList-c11n-8-109-3__sc-1j0som5-0")
            if details:
                beds_element = details.query_selector("li:nth-child(1)")
                baths_element = details.query_selector("li:nth-child(2)")
                sqft_element = details.query_selector("li:nth-child(3)")
                
                beds = beds_element.inner_text() if beds_element else "N/A"
                baths = baths_element.inner_text() if baths_element else "N/A"
                sqft = sqft_element.inner_text() if sqft_element else "N/A"
            else:
                beds, baths, sqft = "N/A", "N/A", "N/A"

            data.append({
                "Price": price.strip(),
                "Address": address.strip(),
                "Beds": beds.strip(),
                "Baths": baths.strip(),
                "Sqft": sqft.strip()
            })

        browser.close()
        return pd.DataFrame(data)

def save_to_db(df):
    if df.empty:
        print("No data to save.")
        return
    
    conn = sqlite3.connect("database.db")
    try:
        conn.execute("DROP TABLE IF EXISTS listings")
        
        df.to_sql("listings", conn, if_exists="append", index=False)
        print("Data saved to database.")
    except Exception as e:
        print(f"Error saving to database: {e}")
    finally:
        conn.commit()
        conn.close()

# Main function
if __name__ == "__main__":
    zip_code = "85308" 
    radius = 10 
    
    data = scrape_listings(zip_code, radius)
    print(data)
    
    if not data.empty:
        save_to_db(data)
        print("Scraping complete!")
    else:
        print("No data found. Check the scraping logic.")