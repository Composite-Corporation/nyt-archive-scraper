from bs4 import BeautifulSoup
from dotenv import load_dotenv
import pandas as pd
import requests
import time
import os

# Load environment variables
load_dotenv()
COOKIE = os.getenv("COOKIE")
USER_AGENT = os.getenv("USER_AGENT")

# Scraping function for NYT archive url
def scrape_nyt_archive_url(url: str) -> str | None:
    # Attempt retrieving web page
    try:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Cookie': COOKIE,
            'User-Agent': USER_AGENT,
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e)
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Retrieve all <p> tags with the specified class name
    paragraphs = soup.find_all('p', class_='css-at9mc1 evys1bk0')

    # Combine the text from all retrieved <p> tags into a single string
    combined_text = '\n'.join([p.get_text() for p in paragraphs])

    print(f"Successfully scraped: {url}")    
    return combined_text


if __name__ == "__main__":
    # Read the Excel file from input folder
    excel_file = pd.ExcelFile('input/all_nyt_links_v2.xlsx')
    
    # Create a dictionary to hold DataFrames for each sheet
    df_dict = {}
    
    # Iterate through each sheet in the Excel file
    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        # Check if 'Scraped Text' column already exists
        if 'Scraped Text' not in df.columns:
            df['Scraped Text'] = df['URL'].apply(lambda url: (time.sleep(0.1), scrape_nyt_archive_url(url))[1])
        else: 
            # Only scrape if 'Scraped Text' is None or an empty string
            df['Scraped Text'] = df.apply(lambda row: (time.sleep(0.1), scrape_nyt_archive_url(row['URL']))[1] if pd.isna(row['Scraped Text']) or row['Scraped Text'] == '' else row['Scraped Text'], axis=1)
        
        # Store the updated DataFrame in the dictionary
        df_dict[sheet_name] = df
    
    # Optionally, save the updated DataFrames to a new Excel file with the same sheets
    with pd.ExcelWriter('output/all_nyt_links_v2_scraped.xlsx') as writer:
        for sheet_name, df in df_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
