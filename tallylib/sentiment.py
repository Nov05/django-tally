# tallylib/sentiment.py
import json


def yelpReviewSentiment(business_id):
    result = '''\
[
    {"subject":"Subject 1", "data1":45, "data2":70, "maxValue":150},
    {"subject":"Subject 2", "data1":75, "data2":95, "maxValue":150},
    {"subject":"Subject 3", "data1":20, "data2":50, "maxValue":150},
    {"subject":"Example Subject 4", "data1":65, "data2":85, "maxValue":150},
    {"subject":"Food", "data1": 35, "data2":45, "maxValue":150}
]
'''

    return json.loads(result)