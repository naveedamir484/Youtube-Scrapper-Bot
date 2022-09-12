from abc import ABC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import time
from tqdm import tqdm

DRIVER_PATH = '../../../../../../Program Files (x86)/chromedriver.exe'

class ScrapperBase(ABC):

    def __init__(self):
        self.driver = None

    def setupWebDriver(self, link):

        try:
            self.driver = webdriver.Chrome(service=Service(DRIVER_PATH))
            self.driver.get(link)
            print("Initiating Scrapping Process for ", self.driver.title, "\n")
            self.driver.implicitly_wait(4)

        except Exception as ex:
            print("link is not accessible ", ex)
            return


    def _scroll_pages(self, scroll_count=120) -> None:

        """ This function is responsible for scrolling the feed to load more data as per the scroll_count. """

        pbar = tqdm(total=100, ncols=100, desc="scrolling pages ")
        page = self.driver.find_element(By.TAG_NAME, "html")
        index = 0
        while True:

            height_before = self.driver.execute_script("return document.documentElement.scrollHeight")
            page.send_keys(Keys.END)
            time.sleep(4)
            height_after = self.driver.execute_script("return document.documentElement.scrollHeight")
            index = index + 1
            if pbar.n <= 85:
                pbar.update(5)
            if height_before == height_after or index == int(scroll_count):
                break

        p_remain = 100 - pbar.n
        pbar.update(p_remain)
        pbar.close()

    @staticmethod
    def progress_bar(msg: str) -> None:

        """ a utility static function helps in monitoring the task by displaying progress bar"""

        pbar = tqdm(total=100, ncols=100, desc=f"{msg}")
        for _ in range(5):
            time.sleep(.2)
            pbar.update(20)
        pbar.close()
