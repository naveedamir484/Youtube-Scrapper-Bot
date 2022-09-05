from src.scrapper import Scrapper
from src.channel_scrapper import ChannelScrapper
from pprint import pprint

####----------- To Scrape everything related to a provided keyword -------------------------------#####

""" Here we can scrape one thing at a time either we can scrape videos, playlists or channel """
""" Scroll count will scroll the page  that many times. if we dont pass scroll_count argument than it will consider infinite scroll """
""" Once the task is completed. It will generate add the data converted into CSV file formate in a same root directory """

# type = 1   for scrapping video or movies
# type = 2   for scrapping playlists
# type = 3   for scraping channels

#####----------------------- To Scrape a Particular Channel ------------------------------------------#####

""" This will return all the data related to this particular channel , 
such as channel name, total videos uploaded with name, links and views,
 total subscriber count and  a list for all the playlist created.... In Json format """

""" output json_obj = {
    "Channel_name": channel_name,
    "Channel_link": channel_link,
    "Subscriber_count": subs_count,
    "Total_views": total_views,
    "Description": desc,
    "Videos": video_dict [ name, link, views] ,
    "Playlists": playlist_dict [ name , link ] } """

def validate(scroll_count) -> bool:

    if scroll_count.isnumeric():
        return True
    else:
        print("Scroll count should be numeric")
        return False

def modes() -> str:

    while True:
        print("Press the key to Choose the MODE ")
        print("1 : Scrape Using Keywords ")
        print("2 : Scrape Using Channel Link ")
        print("3 : Exit")
        val = input()

        if val == "1" or val == "2" or val == "3":
            return val
        else:
            print("Please Choose Valid Options...! ")

def search_keyword() -> None:

    while True:

        print("Press 1 : For scrapping Video OR Movie ")
        print("Press 2 : For scrapping Playlist ")
        print("Press 3 : For scrapping Channel ")
        print("Press 4 : Back ")
        search_type = input()

        if search_type == "1":
            scroll_count = input("Please Enter the Scroll Count ")
            keyword = input("Enter the keywords to Search ")
            if validate(scroll_count):
                Scrapper(keyword, search_type, scroll_count)

        elif search_type == "2":
            scroll_count = input("Please Enter the Scroll Count ")
            keyword = input("Enter the keywords to Search ")
            if validate(scroll_count):
                Scrapper(keyword, search_type, scroll_count)

        elif search_type == "3":
            scroll_count = input("Please Enter the Scroll Count ")
            keyword = input("Enter the keywords to Search ")
            if validate(scroll_count):
                Scrapper(keyword, search_type, scroll_count)

        elif search_type == "4":
            break

        else:
            print("Please Choose Valid Options...! ")

def search_link() -> None:

    link = input("Enter the Channel Link to proceed ")
    search = ChannelScrapper(link)
    pprint(search.get_json())

def execute() -> None:

    while True:
        mode_type = modes()
        if mode_type == "1":
            search_keyword()
        elif mode_type == "2":
            search_link()
        else:
            break


execute()


#
# Scrapper("eminem", "2", 2)
# Scrapper("eminem", "1", 2)
# Scrapper("eminem", "3", 2)
# bot2 = ChannelScrapper("https://www.youtube.com/channel/UCGaYiIpVOEzUWWS9A1zrodQ")
# json_data = bot2.get_json()
# pprint(json_data)
