# jobs/tasks.py
from datetime import datetime
import time
import random
import json
# Local imports
from tallylib.scraper import yelpScraper
from tallylib.sql import getTallyBusiness
from tallylib.sql import getLatestYelpReviewLog
from tallylib.sql import insertYelpReviewLog
from tallylib.sql import updateYelpReviews
from tallylib.sql import insertJobLogs
from tallylib.sql import updateVizdata
from tallylib.sql import insertVizdataLog
from tallylib.sql import checkVizdataTimestamp
from tallylib.textrank import yelpTrendyPhrases
from tallylib.scattertxt import getDataViztype0
from tallylib.statistics import yelpReviewCountMonthly


# job_type = 0
def task_yelpScraper(business_ids=None, 
                     job_type=0):

    if business_ids is None:
        business_ids = getTallyBusiness() # return a list of strings

    for business_id in business_ids:
        print(f"scraping business ID {business_id}...")

        ## get review date range to scrape, e.g.
        # date_range = (datetime.strptime('2018-06-28', '%Y-%m-%d'),
        #               datetime.strptime('2018-07-01', '%Y-%m-%d'))
        yelp_review_log = getLatestYelpReviewLog(business_id)
        if not yelp_review_log:
            date_range = None
            m1 = "for all dates"
        else:
            date_range = (yelp_review_log[0][0], datetime.now())
            m1 = f"from {date_range[0].strftime('%Y-%m-%d')} to {date_range[1].strftime('%Y-%m-%d')}"
        print(f"scraping {m1}")
        
        # scrape Yelp reviews
        status_code, data = None, []
        status_code, data = yelpScraper(business_id, date_range=date_range)
        if status_code==200:
            returncode = updateYelpReviews(business_id, data)
            job_message = f"status code {status_code}, scraped total {len(data)} reviews, {m1}"
            insertJobLogs(business_id, job_type, returncode, job_message)
            if len(data) > 0:
                insertYelpReviewLog(business_id, data[0][0]) # date
        else:
            job_message = f"status code {status_code}"
            if status_code==503: # this is special case for web scraping...
                job_message += " Wasn't able to assign an unblocked proxy IP"
            insertJobLogs(business_id, job_type, 1, job_message)
        print(job_message)

        ## avoid getting blocked if not using a large proxy pool
        # time.sleep(random.uniform(5,20))


# job_type = 1
# 2020-01-22 for 73 cafes in Arizona, it took about 1079 seconds 
#     to generate JSON data for 4 viztypes (viztype 0 to 3)
def task_getVizdata():
    '''
    Generate visualization data by background jobs for better user experience
    '''
    business_ids = []
    business_ids = getTallyBusiness() # return a list of strings

    for business_id in business_ids:

        # viztype 0 and 3 
        # 2020-01-22 viztype 0 and 3 are sharing an API for historical reasons.
        #     if have time, please change it
        viztype = 0
        count = checkVizdataTimestamp(business_id, 0, 14)
        if count == 0:
            vizdata = json.dumps(getDataViztype0(business_id),
                                 sort_keys=False)
            updateVizdata(business_id, viztype, vizdata)
            insertVizdataLog(business_id, viztype, triggeredby=0) # triggered by job

        # viztype 1
        viztype = 1
        count = checkVizdataTimestamp(business_id, 1, 14)
        if count == 0:
            vizdata = json.dumps(yelpTrendyPhrases(business_id), 
                                 sort_keys=False)
            updateVizdata(business_id, viztype, vizdata)
            insertVizdataLog(business_id, viztype, triggeredby=0) # triggered by job

        # viztype 2
        viztype = 2
        count = checkVizdataTimestamp(business_id, 2, 14)
        if count == 0:
            vizdata = json.dumps(yelpReviewCountMonthly(business_id), 
                                 sort_keys=False)
            updateVizdata(business_id, viztype, vizdata)
            insertVizdataLog(business_id, viztype, triggeredby=0) # triggered by job

        # insert a log for the task
        job_message = "Updated viztype 0,1,2,3"
        insertJobLogs(business_id, 1, 0, job_message)
    


