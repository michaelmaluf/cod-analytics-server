from datetime import datetime
from typing import List
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
import app.const as const


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

    def load_matches_page(self):
        self.driver.get(const.BREAKING_POINT_URL)
        time.sleep(3)
        completed_matches_tab = self.driver.find_element(By.CSS_SELECTOR, '.mantine-Button-root.mantine-v2qes1')
        completed_matches_tab.click()
        time.sleep(2)
        self.load_all_matches()

    def load_all_matches(self):
        try:
            load_more_matches_button = self.driver.find_elements(By.CSS_SELECTOR, 'button.mantine-ndf8f2')[1]
            load_more_matches_button.click()
            self.load_all_matches()
        except IndexError:
            print('Matches page has been loaded.')

    ## DEPRECATED: No longer using match dates to query match urls
    # def fetch_match_urls_from_match_dates(self, match_date_urls: List[str]) -> List[str]:
    #     # matches are grouped by their dates, this method scrapes the match urls for each date
    #
    #     match_urls = []
    #     for match_date_url in match_date_urls:
    #         self.driver.get(match_date_url)
    #         time.sleep(3)
    #         match_divs = self.driver.find_elements(By.CLASS_NAME, 'mantine-vdx6qn')
    #
    #         for match_div in match_divs:
    #             anchor_tag = match_div.find_element(By.TAG_NAME, 'a')
    #             match_path = anchor_tag.get_attribute('href')
    #             match_urls.append(match_path)
    #
    #     return match_urls

    def fetch_match_urls_from_last_match_date(self, last_match_date) -> List[str]:

        match_urls = []
        self.load_matches_page()

        match_dates_container = self.driver.find_element(By.CSS_SELECTOR, 'div.mantine-1vj6irj')
        match_date_divs = match_dates_container.find_elements(By.XPATH, './div')

        for match_date_div in match_date_divs:
            match_date = match_date_div.find_element(By.CSS_SELECTOR, 'div.mantine-195cjfh').text
            match_date_object = datetime.strptime(match_date.split(' - ')[1], "%B %d, %Y")

            # scrape matches from last match date until present
            # once we are up to date with the last match, exit loop
            if match_date_object.date() <= last_match_date.date():
                break

            match_divs = match_date_div.find_elements(By.CLASS_NAME, 'mantine-vdx6qn')

            for match_div in match_divs:
                anchor_tag = match_div.find_element(By.XPATH, './a')
                match_path = anchor_tag.get_attribute('href')
                match_urls.append(match_path)

        return match_urls

    def fetch_match_page_source(self, match_url: str):
        self.driver.get(match_url)
        time.sleep(3)
        return self.driver.page_source

    def exit_driver(self):
        self.driver.quit()
        self._driver = None
