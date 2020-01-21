# tallylib/logs.py
import json
import pandas as pd
from datetime import datetime
# Local imports
from tallylib.sql import getJobLogs


def getViewJobLogs(business_id, num):
    if not num or num==None:
        num = 100
    ## a list of tuples
    data = getJobLogs(business_id, num)
    ## return JSON format
    # results = [[
    #     {'uuid': str(d[0])},
    #     {'business_id': d[1]},
    #     {'job_type': d[2]},
    #     {'job_status': d[3]},
    #     {'timestamp': d[4].strftime('%Y-%m-%d')}
    #     ] for d in data]
    # return json.dumps(results)
    return pd.DataFrame(data, columns=['uuid', 
                                       'business_id',
                                       'job_type',
                                       'job_status',
                                       'timestamp',
                                       'job_message'
                                       ]).to_html()