from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import csv
from prettytable import PrettyTable
from tqdm import tqdm
driver_path = '../../../../../../Program Files (x86)/chromedriver.exe'


class Scrapper:

    # use to store the all the filter keywords along with the HTML dom element.
    filter_dict = dict()
    index_dict = dict()

    def __init__(self, keyword, mode_type, scroll_count):

        """ a constructor helps in initialising the instantiated object. """

        self.mode_type = mode_type
        self.scroll_count = scroll_count
        self.keyword = keyword

        self.driver = webdriver.Chrome(service=Service(driver_path))
        self.driver.get(f"https://www.youtube.com/search?q={keyword}")
        print("Initiating Scrapping Process for ", self.driver.title, "\n")
        self.driver.implicitly_wait(4)

        self.fetch_filters()
        self.display_filters()
        self.main()

    @staticmethod
    def progress_bar(msg) -> None:

        """ a utility static function helps in monitoring the task by displaying progress bar"""

        pbar = tqdm(total=100, ncols=100, desc=f"{msg}")
        for _ in range(5):
            time.sleep(.2)
            pbar.update(20)
        pbar.close()

    def initialise_filters(self) -> None:

        if self.mode_type == "1":
            self.add_filter("Video")
        elif self.mode_type == "2":
            self.add_filter("Playlist")
        elif self.mode_type == "3":
            self.add_filter("Channel")

    def fetch_filters(self) -> None:

        """ This function loads the first page and fetch the filter and store the dictionary """

        try:
            filter_menu = self.driver.find_element(By.CSS_SELECTOR, 'div[id="filter-menu"]')
            filter_button = filter_menu.find_element(By.CSS_SELECTOR, 'tp-yt-paper-button[id="button"]')
            filter_button.click()
            atag_cards = self.driver.find_elements(By.TAG_NAME, 'ytd-search-filter-renderer')
        except:
            print("Error in fetching filters")
            return

        for filter_tag in tqdm(atag_cards, ncols=100, desc="fetching filters "):
            a_tag = filter_tag.find_element(By.CSS_SELECTOR, 'a[id="endpoint"]')
            text = a_tag.text
            self.filter_dict[str(text)] = a_tag

        filter_button.click()

    def display_filters(self) -> None:

        """ display all filters available."""

        table = PrettyTable(["Filter Name", "Filter key"])
        for index, value in enumerate(self.filter_dict.keys()):
            table.add_row([value, index + 1])
            self.index_dict[str(index + 1)] = value

        print("Filter Available TO apply ")
        print(table, "\n")
        time.sleep(.3)

        self.progress_bar("Initialising Filters ")
        self.initialise_filters()
        self.input_filters()

    def input_filters(self) -> None:

        """ Utility function for filter selection and its console based Ui. """

        while True:
            print("Enter the filter key to apply filters")
            print("Press Q to continue")
            filter_key = input().lower()

            if filter_key == "Q" or filter_key == "q":
                return
            elif filter_key in self.index_dict:

                self.add_filter(self.index_dict[filter_key])
                result_count = self.match_found()

                print(f"Total {result_count} matches are found...! on first page")

                if result_count == 0:
                    self.driver.quit()
                    break

            else:
                print("Enter valid Key....")

    def match_found(self) -> int:

        """ provides the total match count for particular scrapping mode, after applying filter. """

        try:

            if self.mode_type == "1":
                get_div = self.driver.find_element(By.ID, "contents")
                cards = get_div.find_elements(By.TAG_NAME, "ytd-video-renderer")
                return len(cards)

            elif self.mode_type == "2":
                get_div = self.driver.find_element(By.ID, "contents")
                cards = get_div.find_elements(By.TAG_NAME, "ytd-playlist-renderer")
                return len(cards)

            else:
                get_div = self.driver.find_element(By.ID, "contents")
                cards = get_div.find_elements(By.TAG_NAME, "ytd-channel-renderer")
                return len(cards)

        except:
            print("Error in finding matches ")
            return 0


    def add_filter(self, keyword) -> None:

        """  Add the filter just by passing the keyword of filter to be applied. """

        self.progress_bar(f"adding filter '{keyword}' ")

        try:
            filter_menu = self.driver.find_element(By.CSS_SELECTOR, 'div[id="filter-menu"]')
            filter_button = filter_menu.find_element(By.CSS_SELECTOR, 'tp-yt-paper-button[id="button"]')
            filter_button.click()
            self.filter_dict[keyword].click()
            filter_button.click()
            time.sleep(4)

            print(f"'{keyword}' filter added Successfully !")

        except:
            print("This filter cant be activated at Present")

    def scroll_pages(self) -> None:

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
            if height_before == height_after or index == int(self.scroll_count):
                break

        p_remain = 100 - pbar.n
        pbar.update(p_remain)
        pbar.close()

    def scrape_videos(self) -> None:

        """ This function scrape all the video listed after the scroll is done. And save the data into CSV file. """

        self.scroll_pages()

        try:
            getdiv = self.driver.find_element(By.ID, "contents")
            cards = getdiv.find_elements(By.TAG_NAME, "ytd-video-renderer")
        except:
            print("Error in fetching content in scrape_video ")
            return

        print(f"{len(cards)} records are found !!!")
        time.sleep(.5)
        if len(cards) == 0:
            return

        csv_file = open(f'./Output/{self.keyword}_Videos.csv', 'w', encoding="utf-8")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['S.NO', 'Video Title', 'Video_link', 'Views', 'Uploaded', 'Channel Name', 'Channel Link'])

        for index, card in enumerate(tqdm(cards, ncols=100, desc="scraping videos "), 1):

            try:
                videoLink = card.find_element(By.CSS_SELECTOR, 'a[id="thumbnail"]').get_attribute("href").strip()
                videoTitle = card.find_element(By.CSS_SELECTOR, 'div[id="title-wrapper"]').text.strip()
                Timeline = card.find_element(By.CSS_SELECTOR, 'div[id="metadata-line"]')
                Time_view = Timeline.find_elements(By.TAG_NAME, "span")
                views = Time_view[0].text.strip()
                uploaded = Time_view[1].text.strip()
                channel = card.find_element(By.CSS_SELECTOR, 'yt-formatted-string[id="text"]')
                channelLink = channel.find_element(By.TAG_NAME, 'a').get_attribute("href").strip()
                channelName = channel.find_element(By.TAG_NAME, 'a').get_attribute("innerHTML").strip()

                csv_writer.writerow([index, videoTitle, videoLink, views, uploaded, channelName, channelLink])

            except:
                csv_writer.writerow([index, videoTitle, videoLink, views, "NA", channelName, channelLink])

        csv_file.close()

    def scrape_playlists(self) -> None:

        """ This function scrape all the Playlists and related information. And save the data into CSV file in separate file. """

        self.scroll_pages()


        try:
            getdiv = self.driver.find_element(By.ID, "contents")
            cards = getdiv.find_elements(By.TAG_NAME, "ytd-playlist-renderer")
        except:
            print("Error in fetching content in scrape_playlists ")
            return


        print(f"{len(cards)} records are found !!!")
        time.sleep(.5)
        if len(cards) == 0:
            return

        csv_file = open(f'./Output/{self.keyword}_Playlists.csv', 'w', encoding="utf-8")
        csv_writer = csv.writer(csv_file)
        # header pass as argument to write
        csv_writer.writerow(['S.NO', 'Playlist Title', 'Playlist link', 'Channel Name', 'Channel Link'])

        for index, card in enumerate(tqdm(cards, ncols=100, desc="scrapping playlists "), 1):

            try:
                content = card.find_element(By.CSS_SELECTOR, 'div[id="content"]')
                a_tag = content.find_element(By.TAG_NAME, 'a')
                playlist_link = a_tag.get_attribute("href").strip()
                playlist_name = str(
                    a_tag.find_element(By.CSS_SELECTOR, 'span[id="video-title"]').get_attribute("innerHTML")).strip()

                channel_tag = a_tag.find_element(By.TAG_NAME, 'a')
                channel_link = channel_tag.get_attribute("href").strip()
                channel_name = channel_tag.get_attribute("innerHTML").strip()

                csv_writer.writerow([index, playlist_name, playlist_link, channel_name, channel_link])

            except:
                pass

        csv_file.close()

    def scrape_channels(self) -> None:

        """ This function scrape all the channel found related to a keyword. Further, save the data into CSV file."""

        self.scroll_pages()

        try:
            getdiv = self.driver.find_element(By.ID, "contents")
            cards = getdiv.find_elements(By.TAG_NAME, "ytd-channel-renderer")
        except:
            print("Error in fetching content in scrape_playlists ")
            return

        print(f"{len(cards)} records are found !!!")
        time.sleep(.5)
        if len(cards) == 0:
            return

        csv_file = open(f'./Output/{self.keyword}_Channels.csv', 'w', encoding="utf-8")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['S.NO', 'Channel name', 'Channel link', 'Subscriber', 'Video count'])

        for ind, card in enumerate(tqdm(cards, ncols=100, desc="scrapping channels "), 1):

            try:
                content = card.find_element(By.CSS_SELECTOR, 'div[id="info-section"]')
                a_tag = content.find_element(By.CSS_SELECTOR, 'a[id="main-link"]')
                channel_link = a_tag.get_attribute("href").strip()
                channel_name = a_tag.find_element(By.CSS_SELECTOR, 'yt-formatted-string[id="text"]').get_attribute(
                    "innerHTML").strip()
                meta_data = a_tag.find_element(By.CSS_SELECTOR, 'div[id="metadata"]')
                subscriber = meta_data.find_element(By.CSS_SELECTOR, 'span[id="subscribers"]').get_attribute(
                    "innerHTML").strip()
                video_count = meta_data.find_element(By.CSS_SELECTOR, 'span[id="video-count"]').get_attribute(
                    "innerHTML").strip()

                csv_writer.writerow([ind, channel_name, channel_link, subscriber, video_count])

            except:
                pass

        csv_file.close()

    def main(self) -> None:

        """ main function that is required to triggers first for scrapping any sort of data. """

        if self.mode_type == "1":
            self.scrape_videos()
        elif self.mode_type == "2":
            self.scrape_playlists()
        elif self.mode_type == "3":
            self.scrape_channels()

        self.driver.quit()
        print("\n", "####---------------FINISHED------------------####")
