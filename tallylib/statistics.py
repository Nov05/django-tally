# tallylib.statistics.py
from calendar import monthrange
# Local imports
from tallylib.sql import getReviewCountMonthly


# viztype2
def yelpReviewCountMonthly(business_id):
    data = getReviewCountMonthly(business_id)
    result = []
    for d in data:
        row = dict()
        # YYYY-MM-DD, d[0] is year, d[1] is month
        row['date'] = f'{d[0]}-{d[1]}-{monthrange(d[0], d[1])[1]}'
        row['reviews'] = d[2]
        result.append(row)
    return result
