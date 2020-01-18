import ssl
import urllib.request as request
from concurrent.futures import ThreadPoolExecutor as Executor
from requests import Session
from lxml import html
import pandas as pd
from datetime import datetime
import time
import random


# 2020-01-17 Added review_id, user_id
def yelpScraper(business_id):
    base_url = "https://www.yelp.com/biz/" # add business id
    api_url = "/review_feed?sort_by=date_desc&start=" # add number

    results = []
    for n in range(1):
        with Session() as s:
            url = base_url + business_id + api_url + str(n*20)    
            with s.get(url, timeout=5) as r:    
                if r.status_code==200:
                    response = dict(r.json()) 
                    _html = html.fromstring(response['review_list']) 
                    dates = _html.xpath("//div[@class='review-content']/descendant::span[@class='rating-qualifier']/text()")
                    dates = [datetime.strptime(d.strip(), format("%m/%d/%Y")) for d in dates]
                    stars = _html.xpath("//div[@class='review-content']/descendant::div[@class='biz-rating__stars']/div/@title")
                    stars = [float(s.split(' ')[0]) for s in stars]
                    texts = [e.text for e in _html.xpath("//div[@class='review-content']/p")]
                    review_ids = _html.xpath("//div[@class='review review--with-sidebar']/@data-review-id")
                    user_ids = [s.split(':')[1] for s in _html.xpath("//div[@class='review review--with-sidebar']/@data-signup-object")]
                    results = results + [[date, star, text, review_id, user_id] 
                        for date, star, text, review_id, user_id in zip(dates, stars, texts, review_ids, user_ids)]
        time.sleep(random.uniform(0.1, 0.5))    
    return results


def ApifyRequest():
    # found at https://my.apify.com/proxy
    APIFY_KEY = 'DQHWWRuHxtMkidzYN9n8zskWB'
    url_proxy = f"http://groups-RESIDENTIAL:{APIFY_KEY}@proxy.apify.com:8000"
    proxy_handler = request.ProxyHandler({
        'http': url_proxy,
        'https': url_proxy,
    })

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    httpHandler = request.HTTPSHandler(context=ctx)

    opener = request.build_opener(httpHandler,proxy_handler)
    print(opener.open('https://api.apify.com/v2/browser-info').read())


# Do NOT use this function for its multi-threading execution could 
# easily get the AWS IPs blocked.
def yelpScraperAsync(business_id):
    '''Takes a Yelp business id, scrape site for reviews
    '''
    base_url = "https://www.yelp.com/biz/" # add business id
    api_url = "/review_feed?sort_by=date_desc&start=" # add number

    class Scraper():
        def __init__(self):
            self.data = pd.DataFrame()

        def get_data(self, n, business_id=business_id):
            with Session() as s:
                url = base_url + business_id + api_url + str(n*20)
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

        def scrape(self): 
            # multithreaded execution
            with Executor(max_workers=40) as e:
                list(e.map(self.get_data, range(10)))

    s = Scraper()
    s.scrape()
    return s.data