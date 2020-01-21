# jobs/tasks.py
from datetime import datetime
from datetime import date
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


    for business_id in business_ids[6:7]:
        print(f"scraping business ID {business_id}...")

        # get review date range
        # date_range = (datetime.strptime('2018-06-28', '%Y-%m-%d'),
        #               datetime.strptime('2018-07-01', '%Y-%m-%d'))
        latest_reviews = getLatestYelpReviews(business_id, 1)
        if not latest_reviews:
            date_range = None
        else:
            date_range = (latest_reviews[0][0], date.today())
        print(f"scraping date range {date_range}")

        status_code, data = None, []
        status_code, data = yelpScraper(business_id, date_range=date_range)
        if status_code==200:
            job_message = f"status code {status_code}, total {len(data)} reviews scraped"
            # update table tallyds.yelp_review
            returncode = updateYelpReviews(business_id, data)
            # insert a log for the task
            insertJobLogs(business_id, 0, returncode, job_message)
        time.sleep(random.uniform(3,5))

    return
    




