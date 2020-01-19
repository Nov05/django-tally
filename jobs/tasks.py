# jobs/tasks.py
# Local imports
from tallylib.scraper import yelpScraper
from tallylib.sql import getTallyuserBusiness


# job_type = 0
def task_yelpScraper():
    businesse_ids = getTallyuserBusiness() # a list
    




