import ssl
import urllib.request as request
from concurrent.futures import ThreadPoolExecutor as Executor
from requests import Session
from lxml import html
import pandas as pd
from datetime import datetime
import time
import random


###########################################################################################
# Yelp Scraping
###########################################################################################
# 2020-01-17 Added review_id, user_id
def yelpScrapePage(business_id, 
                   page=0, # page
                   date_range=None # date range
                   ): 
    ''' 
    CAUTION: Do NOT use multi-threading to avoid getting blocked.
    '''
    status_code, results, keep_scraping = None, [], True
    
    base_url = "https://www.yelp.com/biz/" # add business id
    api_url = "/review_feed?sort_by=date_desc&start=" # add number

    with Session() as s:
        url = base_url + business_id + api_url + str(page*20)
        with s.get(url, timeout=5) as r:    
            status_code = r.status_code
            if status_code != 200:
                return status_code, results, keep_scraping

            response = dict(r.json()) 
            _html = html.fromstring(response['pagination'])
            text = _html.xpath("//div[@class='page-of-pages arrange_unit arrange_unit--fill']/text()")
            total_pages = int(text[0].strip().split(' ')[-1])
            if page+1 > total_pages:
                keep_scraping = False
                return status_code, results, keep_scraping
            
            _html = html.fromstring(response['review_list'])
            dates, stars, texts, review_ids, user_ids = [], [], [], [], []
            dates = _html.xpath("//div[@class='review-content']/descendant::span[@class='rating-qualifier']/text()")
            dates = [datetime.strptime(d.strip(), format("%m/%d/%Y")) for d in dates]
            stars = _html.xpath("//div[@class='review-content']/descendant::div[@class='biz-rating__stars']/div/@title")
            stars = [float(s.split(' ')[0]) for s in stars]
            texts = [e.text for e in _html.xpath("//div[@class='review-content']/p")]
            review_ids = _html.xpath("//div[@class='review review--with-sidebar']/@data-review-id")
            user_ids = [s.split(':')[1] for s in _html.xpath("//div[@class='review review--with-sidebar']/@data-signup-object")]
            results = [[date, star, text, review_id, user_id] 
                        for date, star, text, review_id, user_id 
                        in zip(dates, stars, texts, review_ids, user_ids)]
            
            # filter by date
            if date_range is not None:
                idx0, idx1 = None, None
                for i in range(len(dates)):
                    if dates[i]<=date_range[1]:
                        idx0 = i
                        break
                for i in range(len(dates)):
                    if dates[len(dates)-1-i]>=date_range[0]:
                        idx1 = len(dates)-1-i
                        break
                if idx0 is None or idx1 is None or idx1<idx0: 
                    results = []
                else:
                    results = results[idx0:idx1+1]
                    keep_scraping = False

    return status_code, results, keep_scraping


def yelpScraper(business_id,
                date_range=None):
    status_code, results = None, []
    if date_range is not None: print(date_range[0], date_range[1])
        
    for i in range(1000):
        status_code, r, keep_scraping = yelpScrapePage(business_id, 
                                                       page=i, 
                                                       date_range=date_range)
        print('keep scraping:', keep_scraping)
        if status_code != 200:
            return status_code, []
        results = results + r
        if keep_scraping == False:
            break
        # scrape slowly to avoid being blocked
        time.sleep(random.uniform(1, 3))

    return status_code, results



###########################################################################################
# Scraping Proxy
###########################################################################################
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