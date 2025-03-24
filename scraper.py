import pandas as pd
import sqlite3
from playwright.sync_api import sync_playwright
import time
import random

# Scrape real estate listings
def scrape_listings(zip_code, radius):
    # Construct the URL with zip code and radius
    URL = f"https://www.zillow.com/homes/{zip_code}_rb/{radius}_miles/"
    
    with sync_playwright() as p:
        # Launch the browser in non-headless mode for debugging
        browser = p.chromium.launch(headless=False)  # Set headless=True for production
        page = browser.new_page()
        
        # Navigate to the URL
        page.goto(URL)
        
        # Random delay to mimic human behavior
        time.sleep(random.uniform(5, 10))
        
        # Debug: Save the page source to inspect it
        page_source = page.content()
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(page_source)
        
        # Wait for the listings to load
        try:
            page.wait_for_selector(".StyledPropertyCardDataWrapper-c11n-8-109-3__sc-hfbvv9-0", timeout=60000)
        except Exception as e:
            print(f"Error waiting for listings: {e}")
            browser.close()
            return pd.DataFrame()
        
        # Parse the listings
        listings = page.query_selector_all(".StyledPropertyCardDataWrapper-c11n-8-109-3__sc-hfbvv9-0")
        if not listings:
            print("No listings found. Check the page source for anti-bot measures.")
            browser.close()
            return pd.DataFrame()
        
        data = []
        for item in listings:
            # Extract price
            price_element = item.query_selector(".PropertyCardWrapper__StyledPriceLine-srp-8-109-3__sc-16e8gqd-1")
            price = price_element.inner_text() if price_element else "Price not found"
            
            # Extract address
            address_element = item.query_selector("address")
            address = address_element.inner_text() if address_element else "Address not found"
            
            # Extract beds, baths, and sqft
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
            
            # Append to data
            data.append({
                "Price": price.strip(),
                "Address": address.strip(),
                "Beds": beds.strip(),
                "Baths": baths.strip(),
                "Sqft": sqft.strip()
            })
        
        # Close the browser
        browser.close()
        return pd.DataFrame(data)

# Save scraped data to SQLite database
def save_to_db(df):
    if df.empty:
        print("No data to save.")
        return
    
    conn = sqlite3.connect("database.db")
    try:
        # Drop the table if it exists
        conn.execute("DROP TABLE IF EXISTS listings")
        
        # Create the table with the correct schema
        df.to_sql("listings", conn, if_exists="append", index=False)
        print("Data saved to database.")
    except Exception as e:
        print(f"Error saving to database: {e}")
    finally:
        conn.commit()
        conn.close()

# Main function
if __name__ == "__main__":
    # Define the zip code and radius (in miles)
    zip_code = "85308" 
    radius = 10 
    
    # Scrape listings
    data = scrape_listings(zip_code, radius)
    print(data)  # Debug: Print the DataFrame to inspect its contents
    
    # Save to database
    if not data.empty:
        save_to_db(data)
        print("Scraping complete!")
    else:
        print("No data found. Check the scraping logic.")