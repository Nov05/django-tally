# tallylib/logs.py
from datetime import datetime
# Local imports
from tallylib.sql import getLogs

def getViewLogs(business_id, num):
    if not num or num==None:
        num = 100
    # a list of tuples
    data = getLogs(business_id, num)
    results = [[
        {'uuid': str(d[0])},
        {'business_id': d[1]},
        {'job_type': d[2]},
        {'job_status': d[3]},
        {'timestamp': d[4].strftime('%Y-%m-%d')}
        ] for d in data]
    return results