import scrapy
from selenium.webdriver.common.by import By
import pymongo
from selenium import webdriver
from ..items import GetyourguideScrapyItem_LV

DRIVER_FILE_PATH = "/Users/qunishdash/Documents/chromedriver_mac64/chromedriver"

class QuebecLvSpider(scrapy.Spider):
    name = "quebec_lv"
    handle_httpstatus_list = [403]
    start_urls = ["https://www.getyourguide.com/quebec-l561?p=1"]
    page_number = 2

    def __init__(self):
        self.conn = pymongo.MongoClient(
            "localhost",
            27017
        )
        db = self.conn["getyourguide_scrapy_db"]
        self.collection = db["quebec_lv"]

    def get_chrome_driver(self, headless_flag):
        chrome_options = webdriver.ChromeOptions()

        if headless_flag:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--start-maximized")
        else:
            chrome_options.add_argument("--start-maximized")
            chrome_options.headless = False

        driver = webdriver.Chrome(options=chrome_options) 
        return driver
    

    def parse(self, response):
        if response.status == 403:
            self.logger.warning("Status 403 - but chill we are handling using selenium driver.")

        # Initialize the WebDriver here
        driver = self.get_chrome_driver(headless_flag=False)
        driver.get(response.url)

        items = GetyourguideScrapyItem_LV()

        # Extract data using Selenium and yield items
        all_cards = driver.find_elements(By.CSS_SELECTOR, ".activity-card-block__card--grid")

        for card in all_cards:
            try:
                activity_name = card.find_element(By.CSS_SELECTOR, ".vertical-activity-card__title").text
            except Exception as e:
                activity_name = ''
            try:
                activity_type = card.find_element(By.CSS_SELECTOR, ".vertical-activity-card__activity-type").text
            except Exception as e:
                activity_type = ''
            try:
                activity_additional_data = card.find_element(By.CSS_SELECTOR, ".activity-attributes__container").text
            except Exception as e:
                activity_additional_data = ''
            try:
                activity_rating = card.find_element(By.CSS_SELECTOR, ".rating-overall__rating-number--right").text
            except Exception as e:
                activity_rating = ''
            try:
                total_reviews = card.find_element(By.CSS_SELECTOR, ".rating-overall__reviews span").text
            except Exception as e:
                total_reviews = ''
            try:
                activity_price_value = card.find_element(By.CSS_SELECTOR, ".baseline-pricing__value").text
                activity_price_suffix = card.find_element(By.CSS_SELECTOR, ".baseline-pricing__category").text
                activity_price = activity_price_value + " " + activity_price_suffix
            except Exception as e:
                activity_price = ''
            try:
                activity_url = card.find_element(By.CSS_SELECTOR, ".gtm-trigger__card-interaction").get_attribute("href")
            except Exception as e:
                activity_url = ''

            items["activity_name"] = activity_name
            items["activity_type"] = activity_type
            items["activity_additional_data"] = activity_additional_data
            items["activity_rating"] = activity_rating
            items["total_reviews"] = total_reviews
            items["activity_price"] = activity_price
            items["activity_url"] = activity_url

            yield items
            self.collection.insert_one(dict(items))

        next_page = "https://www.getyourguide.com/quebec-l561?p=" + str(self.page_number)
        if self.page_number < 16:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)

        driver.quit()