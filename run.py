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

def choose_Mode() -> str:

    while True:
        print("Press the key to Choose the MODE ")
        print("1 : Scrape Using Keywords ")
        print("2 : Scrape Using Channel Link ")
        print("3 : Exit")
        input1 = input()

        if input1 == "1" or input1 == "2" or input1 == "3":
            return input1
        else:
            print("Please Choose Valid Options...! ")

def choose_options1() -> None:

    while True:

        print("Press 1 : For scrapping Video OR Movie ")
        print("Press 2 : For scrapping Playlist ")
        print("Press 3 : For scrapping Channel ")
        print("Press 4 : Back ")
        input2 = input()

        if input2 == "1":
            scroll_count = input("Please Enter the Scroll Count ")
            keyword = input("Enter the keywords to Search ")
            if validate(scroll_count):
                Scrapper(keyword, input2, scroll_count)

        elif input2 == "2":
            scroll_count = input("Please Enter the Scroll Count ")
            keyword = input("Enter the keywords to Search ")
            if validate(scroll_count):
                Scrapper(keyword, input2, scroll_count)

        elif input2 == "3":
            scroll_count = input("Please Enter the Scroll Count ")
            keyword = input("Enter the keywords to Search ")
            if validate(scroll_count):
                Scrapper(keyword, input2, scroll_count)

        elif input2 == "4":
            break

        else:
            print("Please Choose Valid Options...! ")

def choose_options2() -> None:

    input_link = input("Enter the Channel Link to proceed ")
    bot2 = ChannelScrapper(input_link)
    pprint(bot2.get_json())

def execute() -> None:

    while True:
        input1 = choose_Mode()
        if input1 == "1":
            choose_options1()
        elif input1 == "2":
            choose_options2()
        else:
            break


# execute()

# Scrapper("eminem", "2", 1000)
bot2 = ChannelScrapper("https://www.youtube.com/channel/UCGaYiIpVOEzUWWS9A1zrodQ")
json_data = bot2.get_json()
pprint(json_data)
