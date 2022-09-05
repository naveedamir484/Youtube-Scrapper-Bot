from selenium.webdriver.common.by import By
from src.mode_enum import ModeEnum
import time
import csv
from prettytable import PrettyTable
from tqdm import tqdm
from src.scrapperBase import ScrapperBase


class Search(ScrapperBase):

    # use to store the all the filter keywords along with the HTML dom element.
    filter_dict = {}
    index_dict = {}

    def __init__(self, keyword, mode_type, scroll_count) -> None:
        """ a constructor helps in initialising the instantiated object. """

        self.mode_type = mode_type
        self.scroll_count = scroll_count
        self.keyword = keyword

        if not self._validate():
            return

        super(ScrapperBase, self).__init__()
        super().setupWebDriver(f"https://www.youtube.com/search?q={keyword}")


    def _validate(self) -> bool:

        if not self.mode_type.isnumeric():
            print("mode_type should be numeric ")
            return False

        if not self.scroll_count.isnumeric():
            print("scroll_count should be numeric ")
            return False

        return True


    def search(self) -> None:

        self._add_filters()._main()

    def _add_filters(self):

        self._fetch_filters()
        self._display_filters()
        self._initialise_filters()
        self._filters_util()

        return self

    def _initialise_filters(self) -> None:

        ScrapperBase.progress_bar("Initialising Filters ")

        if self.mode_type == ModeEnum.SEARCH_VIDEOS.value:
            self._add_filter("Video")
        elif self.mode_type == ModeEnum.SEARCH_PLAYLISTS.value:
            self._add_filter("Playlist")
        elif self.mode_type == ModeEnum.SEARCH_CHANNELS.value:
            self._add_filter("Channel")

    def _fetch_filters(self) -> None:

        """ This function loads the first page and fetch the filter and store the dictionary """

        try:
            filter_menu = self.driver.find_element(By.CSS_SELECTOR, 'div[id="filter-menu"]')
            filter_button = filter_menu.find_element(By.CSS_SELECTOR, 'tp-yt-paper-button[id="button"]')
            filter_button.click()
            atag_cards = self.driver.find_elements(By.TAG_NAME, 'ytd-search-filter-renderer')
        except Exception as ex:
            print("Error in fetching filters ", ex)
            return

        for filter_tag in tqdm(atag_cards, ncols=100, desc="fetching filters "):
            a_tag = filter_tag.find_element(By.CSS_SELECTOR, 'a[id="endpoint"]')
            self.filter_dict[str(a_tag.text)] = a_tag

        filter_button.click()

    def _display_filters(self) -> None:

        """ display all filters available."""

        table = PrettyTable(["Filter Name", "Filter key"])
        for index, value in enumerate(self.filter_dict.keys()):
            table.add_row([value, index + 1])
            self.index_dict[str(index + 1)] = value

        print("Filter Available TO apply ")
        print(table, "\n")
        time.sleep(.3)


    def _filters_util(self) -> None:

        """ Utility function for filter selection and its console based Ui. """

        while True:
            print("Enter the filter key to apply filters")
            print("Press Q to continue")
            filter_key = input().lower()

            if filter_key == "Q" or filter_key == "q":
                return
            elif filter_key in self.index_dict:

                self._add_filter(self.index_dict[filter_key])
                result_count = self._match_found()

                print(f"Total {result_count} matches are found...! on first page")

                if result_count == 0:
                    self.driver.quit()
                    break

            else:
                print("Enter valid Key....")

    def _match_found(self) -> int:

        """ provides the total match count for particular scrapping mode, after applying filter. """

        try:

            if self.mode_type == ModeEnum.SEARCH_VIDEOS.value:
                get_div = self.driver.find_element(By.ID, "contents")
                cards = get_div.find_elements(By.TAG_NAME, "ytd-video-renderer")
                return len(cards)

            elif self.mode_type == ModeEnum.SEARCH_PLAYLISTS.value:
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

    def _add_filter(self, keyword) -> None:

        """  Add the filter just by passing the keyword of filter to be applied. """

        ScrapperBase.progress_bar(f"adding filter '{keyword}' ")

        try:
            filter_menu = self.driver.find_element(By.CSS_SELECTOR, 'div[id="filter-menu"]')
            filter_button = filter_menu.find_element(By.CSS_SELECTOR, 'tp-yt-paper-button[id="button"]')
            filter_button.click()
            self.filter_dict[keyword].click()
            filter_button.click()
            time.sleep(4)

            print(f"'{keyword}' filter added Successfully !")

        except Exception as ex:
            print("This filter cant be activated at Present ", ex)


    def _search_videos(self) -> None:

        """ This function search all the video listed after the scroll is done. And save the data into CSV file. """

        self._scroll_pages(self.scroll_count)

        try:
            getdiv = self.driver.find_element(By.ID, "contents")
            cards = getdiv.find_elements(By.TAG_NAME, "ytd-video-renderer")
        except Exception as ex:
            print("Error in fetching content in search video ", ex)
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

                Timeline = card.find_element(By.CSS_SELECTOR, 'div[id="metadata-line"]')
                channel = card.find_element(By.CSS_SELECTOR, 'yt-formatted-string[id="text"]')

                csv_writer.writerow([
                    index,
                    card.find_element(By.CSS_SELECTOR, 'div[id="title-wrapper"]').text.strip(),
                    card.find_element(By.CSS_SELECTOR, 'a[id="thumbnail"]').get_attribute("href").strip(),
                    Timeline.find_elements(By.TAG_NAME, "span")[0].text.strip(),
                    Timeline.find_elements(By.TAG_NAME, "span")[1].text.strip(),
                    channel.find_element(By.TAG_NAME, 'a').get_attribute("innerHTML").strip(),
                    channel.find_element(By.TAG_NAME, 'a').get_attribute("href").strip()
                ])

            except Exception as ex:
                print("Error in card ", ex)

        csv_file.close()

    def _search_playlists(self) -> None:

        """ This function search all the Playlists and related information. And save the data into CSV file in separate file. """

        self._scroll_pages(self.scroll_count)

        try:
            getdiv = self.driver.find_element(By.ID, "contents")
            cards = getdiv.find_elements(By.TAG_NAME, "ytd-playlist-renderer")
        except Exception as ex:
            print("Error in fetching content in search_playlists ", ex)
            return

        print(f"{len(cards)} records are found !!!")
        time.sleep(.5)
        if len(cards) == 0:
            return

        csv_file = open(f'./Output/{self.keyword}_Playlists.csv', 'w', encoding="utf-8")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['S.NO', 'Playlist Title', 'Playlist link', 'Channel Name', 'Channel Link'])

        for index, card in enumerate(tqdm(cards, ncols=100, desc="scrapping playlists "), 1):

            try:
                content = card.find_element(By.CSS_SELECTOR, 'div[id="content"]')
                a_tag = content.find_element(By.TAG_NAME, 'a')
                channel_tag = a_tag.find_element(By.TAG_NAME, 'a')

                csv_writer.writerow([
                    index,
                    a_tag.find_element(By.CSS_SELECTOR, 'span[id="video-title"]').get_attribute("innerHTML").strip(),
                    a_tag.get_attribute("href").strip(),
                    channel_tag.get_attribute("innerHTML").strip(),
                    channel_tag.get_attribute("href").strip()
                ])


            except Exception as ex:
                print("Error in card ", ex)

        csv_file.close()

    def _search_channels(self) -> None:

        """ This function search all the channel found related to a keyword. Further, save the data into CSV file."""

        self._scroll_pages(self.scroll_count)

        try:
            getdiv = self.driver.find_element(By.ID, "contents")
            cards = getdiv.find_elements(By.TAG_NAME, "ytd-channel-renderer")
        except Exception as ex:
            print("Error in fetching content in search_playlists ", ex)
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
                meta_data = a_tag.find_element(By.CSS_SELECTOR, 'div[id="metadata"]')

                csv_writer.writerow([
                    ind,
                    a_tag.find_element(By.CSS_SELECTOR, 'yt-formatted-string[id="text"]').get_attribute(
                        "innerHTML").strip(),
                    a_tag.get_attribute("href").strip(),
                    meta_data.find_element(By.CSS_SELECTOR, 'span[id="subscribers"]').get_attribute(
                        "innerHTML").strip(),
                    meta_data.find_element(By.CSS_SELECTOR, 'span[id="video-count"]').get_attribute(
                        "innerHTML").strip()])


            except Exception as ex:
                print("Error in card ", ex)

        csv_file.close()

    def _main(self) -> None:

        """ main function that is required to triggers first for scrapping any sort of data. """

        # we can use enum for indexing  instead of "1 2  3"

        if self.mode_type == ModeEnum.SEARCH_VIDEOS.value:
            self._search_videos()
        elif self.mode_type == ModeEnum.SEARCH_PLAYLISTS.value:
            self._search_playlists()
        elif self.mode_type == ModeEnum.SEARCH_CHANNELS.value:
            self._search_channels()
        else:
            print("mode_type is incorrect")

        self.driver.quit()

        print("\n", "####---------------FINISHED------------------####")
