import argparse
from src.scrapper import Scrapper
from src.channel_scrapper import ChannelScrapper
from pprint import pprint

parser = argparse.ArgumentParser(description='Youtube Scrapping Bot')
subparser = parser.add_subparsers(dest="command")

mode1 = subparser.add_parser("mode1", help="scraping using keyword")
mode1.add_argument('-d', '--data', type=str, required=True, help="Type of data to Scrape such as : videos, playlists or channels ")
mode1.add_argument('-k', '--keyword', type=str, required=True, help='Text to be searched')
mode1.add_argument('-s', '--scroll_count', type=str, required=True, help='Number of scrolls required')

mode2 = subparser.add_parser("mode2", help="scraping using channel link")
mode2.add_argument('-l', '--channel_link', type=str, required=True, help='Youtube channel link')
args = parser.parse_args()


def function1(mode_type,keyword,scroll_count):
    Scrapper(keyword, mode_type, scroll_count)

def function2(channel_link):
    bot2 = ChannelScrapper(channel_link)
    pprint(bot2.get_json())


if __name__ == '__main__':


    if args.command == "mode1":
        function1(args.data, args.keyword, args.scroll_count)
    elif args.command == "mode2":
        function2(args.channel_link)

