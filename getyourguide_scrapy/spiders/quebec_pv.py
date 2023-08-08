import scrapy
from selenium.webdriver.common.by import By
import pymongo
from selenium import webdriver

DRIVER_FILE_PATH = "/Users/qunishdash/Documents/chromedriver_mac64/chromedriver"

class QuebecPvSpider(scrapy.Spider):
    name = "quebec_pv"
    handle_httpstatus_list = [403]
    allowed_domains = ["example.com"]
    
    def __init__(self):
        self.conn = pymongo.MongoClient(
            "localhost",
            27017
        )
        db = self.conn["getyourguide_scrapy_db"]
        self.collection = db["quebec_lv"]
        self.pvcollection = db["quebec_pv"]

        self.start_urls = [document['activity_url'] for document in self.collection.find()]

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
    
    def get_activity_data(self, url):
        # Initialize the WebDriver here
        driver = self.get_chrome_driver(headless_flag=False)
        driver.get(url)

        try:
            try:
                activity_overview = driver.find_element(By.XPATH, '//*[@id="activity-overview"]/p').text.replace("\n", " ")
            except Exception as e:
                activity_overview = ''
            try:
                activity_details = driver.find_element(By.XPATH, '//*[@id="key-details"]/section/dl').text.replace("\n", " ")
            except Exception as e:
                activity_details = ''
            try:
                activity_description = driver.find_element(By.XPATH, '//*[@id="activity-experience"]/section[2]/div/div[2]/section/div[1]/div').text.replace("\n", " ")
            except Exception as e:
                activity_description = ''
            try:
                activity_experience = driver.find_element(By.XPATH, '//*[@id="activity-experience"]').text.replace("\n", " ")
            except Exception as e:
                activity_experience = ''
            try:
                activity_meeting_point = driver.find_element(By.XPATH, '//*[@id="preparation-info"]/section[1]/div/div[2]/p').text.replace("\n", " ")
            except Exception as e:
                activity_meeting_point = ''
            try:
                activity_important_information = driver.find_element(By.XPATH, '//*[@id="section--important-information"]/div/div[2]').text.replace("\n", " ")
            except Exception as e:
                activity_important_information = ''
            try:
                activity_review_summary = driver.find_element(By.XPATH, '//*[@id="customer-reviews"]/section/div/div[2]/ul').text.replace("\n", " ")
            except Exception as e:
                activity_review_summary = ''
            try:
                activity_includes = driver.find_element(By.XPATH, '//*[@id="activity-experience"]/section[3]/div/div[2]/section/ul[1]').text.replace("\n", " ")
            except Exception as e:
                activity_includes = ''
            try:
                activity_not_includes = driver.find_element(By.XPATH, '//*[@id="activity-experience"]/section[3]/div/div[2]/section/ul[2]').text.replace("\n", " ")
            except Exception as e:
                activity_not_includes = ''
            try:
                activity_provider = driver.find_element(By.XPATH, '//*[@id="main-content"]/section/section[1]/section[4]/div/div/section/div/a').text.replace("\n", " ")
            except Exception as e:
                activity_provider = ''
            try:
                activity_not_suitable_for = driver.find_element(By.XPATH, '//*[@id="not-suitable-for"]/div/div[2]/ul').text.replace("\n", " ")
            except Exception as e:
                activity_not_suitable_for = ''

            data = {
                "activity_url": url,
                "activity_overview": activity_overview,
                "activity_details": activity_details,
                "activity_description": activity_description,
                "activity_experience": activity_experience,
                "activity_meeting_point": activity_meeting_point,
                "activity_important_information": activity_important_information,
                "activity_review_summary": activity_review_summary,
                "activity_includes": activity_includes,
                "activity_not_includes": activity_not_includes,
                "activity_provider": activity_provider,
                "activity_not_suitable_for": activity_not_suitable_for
            }
            return data
        except Exception as e:
            print("Error while extracting activity data:", e)
            return None
        finally:
            driver.quit()

    def parse(self, response):
        if response.status == 403:
            self.logger.warning("Status 403 - but chill we are handling using selenium driver.")
        for url in self.start_urls:
            activity_data = self.get_activity_data(url)
            if activity_data:
                self.pvcollection.update_one({"activity_url": url}, {"$set": activity_data}, upsert=True)
