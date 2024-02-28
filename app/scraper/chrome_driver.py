from typing import List, Dict, Tuple, Optional
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By


class ChromeDriver:
    def __init__(self):
        self.headers = self.get_headers()
        self._driver = None

    def get_headers(self):
        headers = {
            "User-Agent": os.getenv('SCRAPER_USER_AGENT'),
        }
        return headers

    @property
    def driver(self):
        if self._driver is None:
            self._driver = self.initialize_driver()
        return self._driver

    def initialize_driver(self):
        chrome_options = webdriver.ChromeOptions()
        for key, value in self.headers.items():
            chrome_options.add_argument(f"--{key}={value}")
        return webdriver.Chrome(options=chrome_options)

    def fetch_match_urls_from_match_dates(self, match_date_urls: List[str]) -> List[str]:
        # matches are grouped by their dates, this method scrapes the match urls for each date

        match_urls = []
        for match_date_url in match_date_urls:
            self.driver.get(match_date_url)
            time.sleep(3)
            match_divs = self.driver.find_elements(By.CLASS_NAME, 'mantine-vdx6qn')

            for match_div in match_divs:
                anchor_tag = match_div.find_element(By.TAG_NAME, 'a')
                match_path = anchor_tag.get_attribute('href')
                match_urls.append(match_path)

        return match_urls

    def fetch_match_page_source(self, match_url: str):
        self.driver.get(match_url)
        time.sleep(3)
        return self.driver.page_source

    def exit_driver(self):
        self.driver.close()
        _driver = None
