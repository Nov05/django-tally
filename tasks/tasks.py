# jobs/tasks.py
from datetime import datetime
import time
import random
import json
# Local imports
from tallylib.sql import getTallyBusiness
from tallylib.sql import insertTallyBusiness
from tallylib.sql import getLatestYelpReviewLog
from tallylib.sql import insertYelpReviewLog
from tallylib.sql import updateYelpReviews
from tallylib.sql import insertJobLogs
from tallylib.sql import updateVizdata
from tallylib.sql import insertVizdataLog
from tallylib.sql import getVizdataTimestamp
from tallylib.scraper import yelpScraper
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
            if data is not None and len(data) > 0:
                returncode = updateYelpReviews(business_id, data)
                job_message = f"status code {status_code}, scraped total {len(data)} reviews, {m1}"
                insertJobLogs(business_id, job_type, returncode, job_message)
                insertYelpReviewLog(business_id, data[0][0]) # date
                if returncode == 0:
                    insertTallyBusiness([business_id])
        else:
            job_message = f"status code {status_code}"
            if status_code==503: # this is special case for web scraping...
                job_message += " Was not able to assign an unblocked proxy IP"
            insertJobLogs(business_id, job_type, 1, job_message)
        print(job_message)

        ## avoid getting blocked if not using a large proxy pool
        # time.sleep(random.uniform(5,20))


# job_type = 1
# 2020-01-22 for 73 cafes in Arizona, it took about 1079 seconds 
#     to generate JSON data for 4 viztypes (viztype 0 to 3)
def task_getVizdata(business_ids=None):
    '''
    Generate visualization data by background jobs for better user experience
    '''
    if business_ids is None:
        business_ids = []
        business_ids = getTallyBusiness() # return a list of strings

    for business_id in business_ids:
        print(f"Generating visualization data for business ID {business_id}...")

        data = getLatestYelpReviewLog(business_id)
        if len(data) > 0:
            timestamp_yelpreview = data[0][0]
        else:
            print("Visualization data are recent. No need to re-generate.")
            return # no reviews to process

        # viztype 0 and 3 
        # 2020-01-22 viztype 0 and 3 are sharing an API for historical reasons.
        #     if have time, please change it
        viztype = 0
        data = getVizdataTimestamp(business_id, 0)
        if len(data) > 0:
            timestamp_vizdata = data[0][0]
        # If don't get .date(), it will raise 
        # TypeError: can't compare offset-naive and offset-aware datetimes
        if len(data) == 0 or timestamp_vizdata.date() < timestamp_yelpreview.date():
            vizdata = json.dumps(getDataViztype0(business_id),
                                 sort_keys=False)
            if vizdata is not None and len(vizdata) > 0:
                updateVizdata(business_id, viztype, vizdata)
                insertVizdataLog(business_id, viztype, triggeredby=0) # triggered by job

        # viztype 1
        viztype = 1
        data = getVizdataTimestamp(business_id, 1)
        if len(data) > 0:
            timestamp_vizdata = data[0][0]
        if len(data) == 0 or timestamp_vizdata.date() < timestamp_yelpreview.date():
            vizdata = json.dumps(yelpTrendyPhrases(business_id), 
                                 sort_keys=False)
            if vizdata is not None and len(vizdata) > 0:
                updateVizdata(business_id, viztype, vizdata)
                insertVizdataLog(business_id, viztype, triggeredby=0) # triggered by job

        # viztype 2
        viztype = 2
        data = getVizdataTimestamp(business_id, 2)
        if len(data) > 0:
            timestamp_vizdata = data[0][0]
        if len(data) == 0 or timestamp_vizdata.date() < timestamp_yelpreview.date():
            vizdata = json.dumps(yelpReviewCountMonthly(business_id), 
                                 sort_keys=False)
            if vizdata is not None and len(vizdata) > 0:
                updateVizdata(business_id, viztype, vizdata)
                insertVizdataLog(business_id, viztype, triggeredby=0) # triggered by job

        # insert a log for the task
        job_message = "Updated viztype 0,1,2,3"
        print(job_message)
        insertJobLogs(business_id, 1, 0, job_message) # job type 1, success


# jot type = 2 
# 