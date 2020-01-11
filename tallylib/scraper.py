from concurrent.futures import ThreadPoolExecutor as Executor
from requests import Session
from lxml import html
import pandas as pd

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

def yelpScraper(bid):
    '''Takes a url, scrape site for reviews
    and calculates the term frequencies
    sorts and returns the top 10 as a json object
    containing term, highratingscore, poorratingscore.'''

    base_url = "https://www.yelp.com/biz/" # add business id
    api_url = "/review_feed?sort_by=date_desc&start=" # add number

    class Scraper():
        def __init__(self):
            self.data = pd.DataFrame()

        def get_data(self, n, bid=bid):
            with Session() as s:
                url = base_url + bid + api_url + str(n*20)
                with s.get(url, timeout=5) as r: 
                    if r.status_code==200:
                        response = dict(r.json()) 
                        _html = html.fromstring(response['review_list']) 
                        dates = _html.xpath("//div[@class='review-content']/descendant::span[@class='rating-qualifier']/text()")
                        dates = [d.strip() for d in dates]
                        reviews = [e.text for e in _html.xpath("//div[@class='review-content']/p")]
                        ratings = _html.xpath("//div[@class='review-content']/descendant::div[@class='biz-rating__stars']/div/@title")
                        df = pd.DataFrame([dates, reviews, ratings]).T
                        self.data = pd.concat([self.data, df])

        def scrape(self): # makes it faster
            # multithreaded looping
            with Executor(max_workers=40) as e:
                list(e.map(self.get_data, range(10)))

    s = Scraper()
    s.scrape()
    return s.data