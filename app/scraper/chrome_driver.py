from selenium import webdriver

class ChromeDriver:
    def __init__(self):
        self.headers = self.get_headers()
        self._driver = None

    def get_headers(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
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

    def get_webpage(self, url):
        self.driver.get(url)
        webpage = self.driver.page_source
        self.driver.close()
        self._driver = None
        return webpage

