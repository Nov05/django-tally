# tallylib/sql.py
from django.db import connection
# Local
from yelp.models import Review
from jobs.models import JobLogs
'''
2020-01-10 Database table "tallyds.review" has the following index created.
    "CREATE INDEX idx_review ON tallyds.review (business_id, datetime DESC);"
2020-01-15 Database table "tallyds.job_logs has the following index created.
    "
'''

# Query with Django data models
def getReviews(business_id, 
               starting_date, 
               ending_date):
    sql = f'''
    SELECT uuid, date, text FROM tallyds.review
    WHERE business_id = '{business_id}'
    AND datetime >= '{starting_date}'
    AND datetime <= '{ending_date}'
    ORDER BY datetime DESC;
    '''
    return [[record.date, record.text] for record in Review.objects.raw(sql)]


# Query without Django data models
def getReviewCountMonthly(business_id,
                          number_of_months=12):
    sql = f'''
    SELECT extract(year from date)::INTEGER AS year,
           extract(month from date)::INTEGER AS month,
           count(*) AS count
    FROM tallyds.review AS r
    WHERE business_id = '{business_id}'
    GROUP BY 1, 2
    ORDER BY 1 DESC, 2 DESC
    LIMIT {number_of_months};
    '''
    with connection.cursor() as cursor:
        cursor.execute(sql)
        # return a tuple
        return cursor.fetchall()

    
def getLatestReviewDate(business_id):
    sql = f'''
    SELECT datetime
    FROM tallyds.review
    WHERE business_id = '{business_id}'
    ORDER BY datetime DESC
    LIMIT 1;
    '''
    with connection.cursor() as cursor:
        cursor.execute(sql)
        # return a datetime.datatime object
        return cursor.fetchone()[0]

def getLatestReviews(business_id, 
                     limit=200):
    sql = f'''
    SELECT date, 
           text,
           stars::INTEGER
    FROM tallyds.review
    WHERE business_id = '{business_id}'
    ORDER BY datetime DESC
    LIMIT 200;
    '''
    with connection.cursor() as cursor:
        cursor.execute(sql)
        # return a list of tuples
        return cursor.fetchall()

def getLogs(business_id,
            num=100):
    '''
    uuid, 
    business_id,
    job_type,
    job_status,
    timestamp,
    job_message
    '''
    sql = f'''
    SELECT *
    FROM tallyds.job_logs
    WHERE business_id = '{business_id}'
    ORDER BY timestamp DESC
    LIMIT {num};
    '''
    with connection.cursor() as cursor:
        cursor.execute(sql)
        # return a list of tuples
        return cursor.fetchall()

def getTallyuserBusiness():
    sql = '''
    SELECT DISTINCT business_id
    FROM tallyds.tallyuser_business;
    '''
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return [r[0] for r in cursor.fetchall()]