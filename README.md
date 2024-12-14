# TLDR

I already ran the script for you. The code is just here for you in case it's useful for you. Download the Excel file under the "output" folder. The rows that are empty were archives that only contained video/other content that wasn't text.

### Payment Options

1. Venmo: @Leon-Chen-24
2. Cash

# Usage Instructions

### Clone this repository
`git clone https://github.com/Composite-Corporation/nyt-archive-scraper`

### Run setup commands

1. Set up a Python virtual environment
`python3 -m venv venv`

2. Activate your virtual environment
`source venv/bin/activate`

3. Install the required dependencies
`pip install -r requirements.txt`

### Set up web scraper

1. Go to a sample NYTimes archive link, use inspect element, and then click the "Network" tab. Select the request to the article itself. You might need to refresh the page to see this request show up in the tab.

2. Click the request and go to the request headers section. Copy what you see for the "User-Agent" and "Cookie" parameters.

3. In your local repository, create a file named ".env".

4. Add the following items to the file and save:
`USER_AGENT=[INSERT WHAT YOU COPIED]`
`COOKIE=[INSERT WHAT YOU COPIED]`

5. Finally, put the spreadsheet that you want to scrape into the "input" folder. Most importantly, it just needs a "URL" column with all the NYTimes archives you need to scrape the text from.



### Run the script

`python3 scraper.py`

Result will be found in the "output" folder after the script is finished running.
