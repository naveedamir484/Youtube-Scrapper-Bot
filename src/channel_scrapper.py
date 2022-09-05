import json
from pprint import pprint

from selenium.webdriver.common.by import By
from src.scrapperBase import ScrapperBase
from tqdm import tqdm

DRIVER_PATH = '../../../../../../Program Files (x86)/chromedriver.exe'

class ChannelScrapper(ScrapperBase):

    def __init__(self, link) -> None:
        """ a constructor helps in initialising the instantiated object. """

        self.data = {}
        self._link = link

        super(ScrapperBase, self).__init__()
        super().setupWebDriver(link)


    def scrape(self):

        try:
            self.driver.get(self._link)
            self.data["channel link"] = self._link
            print("Initiating Scrapping Process for ", self.driver.title, "\n")
            self.driver.implicitly_wait(4)

        except Exception as ex:
            print("Youtube channel link is not accessible ", ex)
            return

        self._scrape_tabs()._generate_file()

    def _scrape_tabs(self):

        self._fetch_playlists()
        self._fetch_videos()
        self._fetch_channel_name()
        self._fetch_about()

        return self

    def _fetch_channel_name(self) -> None:
        """ this method fetch channel name and subscribers count. """

        try:
            self.progress_bar("fetching channel info ")
            meta = self.driver.find_element(By.CSS_SELECTOR, 'div[id="meta"]')
            channel_name = meta.find_element(By.CSS_SELECTOR, 'yt-formatted-string[id="text"]').text.strip()
            subs_count = meta.find_element(By.CSS_SELECTOR, 'yt-formatted-string[id="subscriber-count"]').text.strip()
            self.data["channel name"] = channel_name
            self.data["subscribers"] = subs_count

        except Exception as ex:
            print("Error in fetching channel information ", ex)



    def _fetch_videos(self) -> None:
        """ this fetches all the video uploaded to particular channel, and store in dictionary. """

        self._tabs_util(1)
        self._scroll_pages()

        try:
            contents = self.driver.find_element(By.CSS_SELECTOR, 'div[id="contents"]')
            cards = contents.find_elements(By.CSS_SELECTOR, 'ytd-grid-video-renderer[class="style-scope ytd-grid-renderer"]')
        except Exception as ex:
            print("Error in fetching content ", ex)
            return

        videos = []

        for card in cards:

            try:
                detail = card.find_element(By.CSS_SELECTOR, 'div[id="details"]')
                video_tag = detail.find_element(By.CSS_SELECTOR, 'a[id="video-title"]')
                metadata_line = card.find_element(By.CSS_SELECTOR, 'div[id="metadata-line"]')
                views_date = metadata_line.find_elements(By.CSS_SELECTOR, 'span[class="style-scope ytd-grid-video-renderer"]')

                videos.append({
                    video_tag.get_attribute("innerHTML").strip(): {
                        "link": video_tag.get_attribute("href"),
                        "views": views_date[0].text.strip(),
                        "uploaded_time":  views_date[1].text.strip()
                    }
                })

            except Exception as ex:
                print("Error in card ", ex)

        self.data["videos"] = videos


    def _fetch_playlists(self) -> None:
        """ this fetches all the playlists uploaded to particular channel, and store in playlist_dictionary. """

        # define all the constants at top
        self._tabs_util(2)
        self._playlist_util(1)
        self._scroll_pages()

        try:
            content = self.driver.find_element(By.CSS_SELECTOR, 'div[id="contents"]')
            css_selector = 'ytd-grid-playlist-renderer[class="style-scope ytd-grid-renderer"]'
            cards = content.find_elements(By.CSS_SELECTOR, css_selector)

        except Exception as ex:
            print("Error in fetching content ", ex)
            return

        playlists = []

        for card in tqdm(cards, ncols=100, desc="scraping playlists "):

            try:
                a_tag = card.find_element(By.CSS_SELECTOR, 'a[id="video-title"]')

                playlists.append({
                    a_tag.get_attribute("innerHTML").strip(): a_tag.get_attribute("href").strip()
                })

            except Exception as ex:
                print("Error in card ", ex)

        self.data["Playlists"] = playlists

    def _get_description(self) -> None:
        """ util function is required during tab switch. """

        stats = self.driver.find_element(By.CSS_SELECTOR, 'div[id="right-column"]').find_elements(By.TAG_NAME, 'yt-formatted-string')

        self.data["total views"] = stats[2].text.strip()
        self.data["joined data"] = stats[1].text.strip()
        self.data["description"] = self.driver.find_element(By.CSS_SELECTOR, 'yt-formatted-string[id="description"]').text

    def _fetch_about(self) -> None:

        """ this fetches ABOUT info in about tab. """

        self.progress_bar("fetching about ")

        try:
            self._tabs_util(4)
            self._get_description()
        except:
            try:
                self._tabs_util(5)
                self._get_description()
            except:
                try:
                    self._tabs_util(6)
                    self._get_description()
                except Exception as ex:
                    print("Error in fetching about ", ex)


    def _tabs_util(self, ind) -> None:
        """ this method responsible for click events such as choosing tabs """

        try:
            tabs = self.driver.find_element(By.CSS_SELECTOR, 'div[id="tabsContent"]')
            tab_button = tabs.find_elements(By.TAG_NAME, 'tp-yt-paper-tab')
            tab_button[ind].click()
        except Exception as ex:
            print("Error in choosing tabs ", ex)


    def _playlist_util(self, ind) -> None:
        """ this method responsible for click events such as choosing playlist """

        try:
            btn = self.driver.find_element(By.CSS_SELECTOR, 'tp-yt-paper-button[id="label"]')
            btn.click()

            dropdown = self.driver.find_element(By.CSS_SELECTOR, 'tp-yt-paper-listbox[id="menu"]')
            options = dropdown.find_elements(By.TAG_NAME, 'a')
            options[ind].click()

        except Exception as ex:
            print("Error in choosing playlist ", ex)



    def _generate_file(self) -> None:
        """ this method converts the python dictionary object into json format and further return it. """

        with open(f"./Output/{self.data['channel name']}_Channel.json", 'w') as fp:
            json.dump(self.data, fp)

        json_data = json.dumps(self.data)
        pprint(json_data)
        self.driver.quit()
