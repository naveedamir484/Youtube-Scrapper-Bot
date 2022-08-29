from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import json
from tqdm import tqdm
driver_path = '../../../../../../Program Files (x86)/chromedriver.exe'


class ChannelScrapper:

    main_dict = dict({"videos": {}, "playlists": {}})

    def __init__(self, keyword) -> None:
        
        """ a constructor helps in initialising the instantiated object. """

        self.driver = webdriver.Chrome(service=Service(driver_path))
        self.driver.get(keyword)
        self.main_dict["channel link"] = keyword
        print("Initiating Scrapping Process for ", self.driver.title, "\n")
        self.driver.implicitly_wait(4)

        self.fetch_playlists()
        self.fetch_videos()
        self.fetch_channel_name()
        self.fetch_about()

    def scroll_pages(self) -> None:

        """ This function is responsible for scrolling the feed to load more data as per the scroll_count. """

        pbar = tqdm(total=100, ncols=100, desc="scrolling pages ")
        page = self.driver.find_element(By.TAG_NAME, "html")
        while True:

            height_before = self.driver.execute_script("return document.documentElement.scrollHeight")
            page.send_keys(Keys.END)
            time.sleep(4)
            height_after = self.driver.execute_script("return document.documentElement.scrollHeight")
            if pbar.n <= 85:
                pbar.update(5)
            if height_before == height_after:
                break

        p_remain = 100 - pbar.n
        pbar.update(p_remain)
        pbar.close()

    @staticmethod
    def progress_bar(msg) -> None:

        """ a utility static function helps in monitoring the task by displaying progress bar """

        pbar = tqdm(total=100, ncols=100, desc=f"{msg}")
        for _ in range(5):
            time.sleep(.2)
            pbar.update(20)
        pbar.close()

    def fetch_channel_name(self) -> None:

        """ this method fetch channel name and subscribers count. """

        try:
            self.progress_bar("fetching channel info ")
            meta = self.driver.find_element(By.CSS_SELECTOR, 'div[id="meta"]')
            channel_name = meta.find_element(By.CSS_SELECTOR, 'yt-formatted-string[id="text"]').text.strip()
            subs_count = meta.find_element(By.CSS_SELECTOR, 'yt-formatted-string[id="subscriber-count"]').text.strip()
            self.main_dict["channel name"] = channel_name
            self.main_dict["subscribers"] = subs_count
        except:
            print("Error in fetching channel information ")


    def playlist_util(self, ind) -> None:

        """ this method responsible for click events such as choosing playlist """

        try:
            btn = self.driver.find_element(By.CSS_SELECTOR, 'tp-yt-paper-button[id="label"]')
            btn.click()

            dropdown = self.driver.find_element(By.CSS_SELECTOR, 'tp-yt-paper-listbox[id="menu"]')
            options = dropdown.find_elements(By.TAG_NAME, 'a')
            options[ind].click()

        except:
            print("Error in choosing playlist ")

    def tabs_util(self, ind) -> None:

        """ this method responsible for click events such as choosing tabs """

        try:
            tabs = self.driver.find_element(By.CSS_SELECTOR, 'div[id="tabsContent"]')
            tab_button = tabs.find_elements(By.TAG_NAME, 'tp-yt-paper-tab')
            tab_button[ind].click()
        except:
            print("Error in choosing tabs ")

    def fetch_videos(self) -> None:

        """ this fetches all the video uploaded to particular channel, and store in dictionary. """

        self.tabs_util(1)
        self.scroll_pages()

        try:
            contents = self.driver.find_element(By.CSS_SELECTOR, 'div[id="contents"]')
            cards = contents.find_elements(By.CSS_SELECTOR, 'ytd-grid-video-renderer[class="style-scope ytd-grid-renderer"]')
        except:
            print("Error in fetching content ")
            return


        for card in cards:

            try:
                detail = card.find_element(By.CSS_SELECTOR, 'div[id="details"]')
                video_tag = detail.find_element(By.CSS_SELECTOR, 'a[id="video-title"]')
                video_link = video_tag.get_attribute("href")
                video_name = video_tag.get_attribute("innerHTML").strip()

                metadata_line = card.find_element(By.CSS_SELECTOR, 'div[id="metadata-line"]')
                views_date = metadata_line.find_elements(By.CSS_SELECTOR, 'span[class="style-scope ytd-grid-video-renderer"]')
                views = views_date[0].text.strip()
                uploaded_time = views_date[1].text.strip()
                self.main_dict["videos"][video_name] = dict({"link": video_link, "views": views, "uploaded_time": uploaded_time})

            except:
                pass



    def fetch_playlists(self) -> None:

        """ this fetches all the playlists uploaded to particular channel, and store in playlist_dictionary. """

        self.tabs_util(2)
        self.playlist_util(1)
        self.scroll_pages()

        try:
            content = self.driver.find_element(By.CSS_SELECTOR, 'div[id="contents"]')
            css_selector = 'ytd-grid-playlist-renderer[class="style-scope ytd-grid-renderer"]'
            cards = content.find_elements(By.CSS_SELECTOR, css_selector)

        except:
            print("Error in fetching content ")
            return


        for card in tqdm(cards, ncols=100, desc="scraping playlists "):

            try:
                a_tag = card.find_element(By.CSS_SELECTOR, 'a[id="video-title"]')
                playlist_name = a_tag.get_attribute("innerHTML").strip()
                playlist_link = a_tag.get_attribute("href").strip()
                self.main_dict["playlists"][playlist_name] = playlist_link

            except:
                pass



    def fetch_util(self) -> None:

        """ util function is required during tab switch. """

        desc = self.driver.find_element(By.CSS_SELECTOR, 'yt-formatted-string[id="description"]').text
        right_box = self.driver.find_element(By.CSS_SELECTOR, 'div[id="right-column"]')
        stats = right_box.find_elements(By.TAG_NAME, 'yt-formatted-string')
        joined_date = stats[1].text.strip()
        total_views = stats[2].text.strip()
        self.main_dict["total views"] = total_views
        self.main_dict["joined data"] = joined_date
        self.main_dict["description"] = desc

    def fetch_about(self) -> None:

        """ this fetches ABOUT info in about tab. """

        self.progress_bar("fetching about ")

        try:
            self.tabs_util(4)
            self.fetch_util()
        except:
            try:
                self.tabs_util(5)
                self.fetch_util()
            except:
                try:
                    self.tabs_util(6)
                    self.fetch_util()
                except:
                    print("Error in fetching about ")


    def get_json(self) -> json:

        """ this method converts the python dictionary object into json format and further return it. """

        with open(f"./Output/{self.main_dict['channel name']}_Channel.json", 'w') as fp:
            json.dump(self.main_dict, fp)

        self.driver.quit()
        return json.dumps(self.main_dict)
