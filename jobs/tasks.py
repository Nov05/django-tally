# jobs/tasks.py
from datetime import datetime
import time
import random
# Local imports
from tallylib.scraper import yelpScraper
from tallylib.sql import getTallyuserBusiness
from tallylib.sql import getLatestYelpReviews
from tallylib.sql import updateYelpReviews
from tallylib.sql import insertJobLogs


# job_type = 0
def task_yelpScraper():

    business_ids = []
    business_ids = getTallyuserBusiness() # return a list of strings

    for business_id in business_ids:
        print(f"scraping business ID {business_id}...")

        ## get review date range to scrape 
        # date_range = (datetime.strptime('2018-06-28', '%Y-%m-%d'),
        #               datetime.strptime('2018-07-01', '%Y-%m-%d'))
        latest_reviews = getLatestYelpReviews(business_id, 1)
        if not latest_reviews:
            date_range = None
            m1 = "for all dates"
        else:
            date_range = (latest_reviews[0][0], datetime.now())
            m1 = f"from {date_range[0].strftime('%Y-%m-%d')} to {date_range[1].strftime('%Y-%m-%d')}"
        print(f"scraping {m1}")
        
        # scrape Yelp reviews
        status_code, data = None, []
        status_code, data = yelpScraper(business_id, date_range=date_range)
        if status_code==200:
            job_message = f"status code {status_code}, scraped total {len(data)} reviews, {m1}"
            # update table tallyds.yelp_review
            returncode = updateYelpReviews(business_id, data)
            # insert a log for the task
            insertJobLogs(business_id, 0, returncode, job_message)
        else:
            job_message = f"status code {status_code}"
            if status_code==503:
                job_message += " possibly got blocked"
            insertJobLogs(business_id, 0, 1, job_message)
        print(job_message)

        ## avoid getting blocked if not using a large proxy pool
        # time.sleep(random.uniform(5,20))


def task_getVizdata():
    pass 
    




