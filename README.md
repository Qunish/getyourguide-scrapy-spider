# Scrapy Spider: QuebecLvSpider and QuebecPvSpider

This repository contains two Scrapy spiders, `QuebecLvSpider` and `QuebecPvSpider`, that are designed to scrape activity data from the GetYourGuide website for the Quebec region. These spiders utilize Selenium for dynamic content rendering and MongoDB for storing the scraped data.

## Requirements

- Python 3.x
- Scrapy
- Selenium
- ChromeDriver
- pymongo

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Qunish/getyourguide-scrapy-based-crawler.git
   cd your-repo
   ```

2. Install the required dependencies using pip:

   ```bash
   pip install scrapy selenium pymongo
   ```

3. Download and install the appropriate ChromeDriver version from [here](https://sites.google.com/chromium.org/driver/).

## Spider Details

### QuebecLvSpider

- Name: `quebec_lv`
- Purpose: This spider scrapes the list view of activities from the GetYourGuide website for the Quebec region.
- How to Run: Execute the following command in the terminal:

  ```bash
  scrapy crawl quebec_lv
  ```

### QuebecPvSpider

- Name: `quebec_pv`
- Purpose: This spider scrapes the details of individual activities from the GetYourGuide website for the Quebec region.
- How to Run: Execute the following command in the terminal:

  ```bash
  scrapy crawl quebec_pv
  ```

## Usage

1. Run the `QuebecLvSpider` to scrape the list view URLs of activities:

   ```bash
   scrapy crawl quebec_lv
   ```

2. After `QuebecLvSpider` has collected the URLs, run the `QuebecPvSpider` to scrape detailed activity information:

   ```bash
   scrapy crawl quebec_pv
   ```

3. The scraped data will be stored in a MongoDB database named `getyourguide_scrapy_db` in collections `quebec_lv` and `quebec_pv` respectively.

## Notes

- Make sure to update the `DRIVER_FILE_PATH` in the spiders with the correct path to your downloaded ChromeDriver executable.
- Adjust XPaths and extraction logic according to the website's structure.
- Check the MongoDB connection settings to ensure proper data storage.