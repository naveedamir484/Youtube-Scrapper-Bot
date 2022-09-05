import argparse
from src.scrapper import Search
from src.channel_scrapper import ChannelScrapper


parser = argparse.ArgumentParser(description='Youtube Scrapping Bot')
subparser = parser.add_subparsers(dest="mode")

search = subparser.add_parser("search", help="searching using keyword")
search.add_argument('-d', '--data', type=str, required=True, help="Type of data to Scrape e.g, videos, playlists or channels ")
search.add_argument('-k', '--keyword', type=str, required=True, help='Keyword to be searched')
search.add_argument('-s', '--scroll_count', type=str, required=True, help='Number of scrolls required')

scrape = subparser.add_parser("scrape", help="scraping using channel link")
scrape.add_argument('-l', '--channel_link', type=str, required=True, help='Youtube channel link')
args = parser.parse_args()


def search_keyword(mode_type, keyword, scroll_count) -> None:
    Search(keyword, mode_type, scroll_count).search()

def scrape_link(channel_link) -> None:
    ChannelScrapper(channel_link).scrape()


if __name__ == '__main__':

    if args.mode == "search":
        search_keyword(args.data, args.keyword, args.scroll_count)
    elif args.mode == "scrape":
        scrape_link(args.channel_link)

# python run.py search -d 1 -k "cyber attacks" -s 2
# python run.py scrape -l https://www.youtube.com/channel/UCGaYiIpVOEzUWWS9A1zrodQ
