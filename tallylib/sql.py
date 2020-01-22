# tallylib/sql.py
from datetime import datetime
from datetime import timedelta
from django.db import connection
# Local
from yelp.models import Review
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
    LIMIT {limit};
    '''
    with connection.cursor() as cursor:
        cursor.execute(sql)
        # return a list of tuples
        return cursor.fetchall()

def getLatestYelpReviews(business_id, 
                     limit=1):
    sql = f'''
    SELECT datetime, 
           text,
           stars::INTEGER
    FROM tallyds.yelp_review
    WHERE business_id = '{business_id}'
    ORDER BY datetime DESC
    LIMIT {limit};
    '''
    with connection.cursor() as cursor:
        cursor.execute(sql)
        # return a list of tuples
        return cursor.fetchall()

def getJobLogs(business_id,
               limit=100):
    # uuid, 
    # business_id,
    # job_type,
    # job_status,
    # timestamp,
    # job_message
    sql = f'''
    SELECT *
    FROM tallyds.job_log
    WHERE business_id = '{business_id}'
    ORDER BY timestamp DESC
    LIMIT {limit};
    '''
    with connection.cursor() as cursor:
        cursor.execute(sql)
        # return a list of tuples
        return cursor.fetchall()


def insertJobLogs(business_id,
                  job_type,
                  job_status,
                  job_message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = f'''\
    INSERT INTO tallyds.job_log
    VALUES (
        uuid_generate_v4(), 
	    '{business_id}',
	    {job_type},
	    {job_status},
	    '{timestamp}',
        '{job_message}'
    );'''
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
    except Exception as e:
        print(sql)
        print(str(e))
        return 1 # returncode failure
    return 0 # returncode success


def updateYelpReviews(business_id, data):
    # data columns: datetime, star, text, review_id, user_id
    if len(data)==0:
        return 0 # returncode success

    s0 = "INSERT INTO tallyds.yelp_review VALUES "
    s1 = ""
    for d in data:
        d_datetime = d[0].strftime('%Y-%m-%d %H:%M:%S')
        d_date = d[0].strftime('%Y-%m-%d')
        d_time = d[0].strftime('%H:%M:%S')
        d_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        d_text = d[2].replace("'", "''")
        s2 = s2 + f"""\n    ('{d[3]}', \
'{business_id}', \
'{d[4]}', \
{d[1]}, \
'{d_datetime}', \
'{d_date}', \
'{d_time}', \
'{d_text}', \
'{d_now}'),"""

#     s2 = '''
# ON CONFLICT ON CONSTRAINT yelp_review_pkey
# DO UPDATE SET
#     business_id = excluded.business_id,
#     user_id = excluded.user_id,
#     stars = excluded.stars,
#     datetime = excluded.datetime,
#     date = excluded.date,
#     time = excluded.time,
#     text = excluded.text,
#     timestamp = excluded.timestamp;    
# '''
    s2 = '''
ON CONFLICT ON CONSTRAINT yelp_review_pkey
DO NOTHING;  
'''
    sql= s0 +s1[:-1] + s2
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
    except Exception as e:
        print(e)
        return 1 # returncode 1 = failure
    return 0 # returncode 0 = success


def getTallyuserBusiness():
    sql = '''
    SELECT DISTINCT business_id
    FROM tallyds.tallyuser_business;
    '''
    with connection.cursor() as cursor:
        cursor.execute(sql)
        # return a list of strings
        return [r[0] for r in cursor.fetchall()]


def updateVizdata(business_id,
                  viztype,
                  vizdata):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql=f'''\
    INSERT INTO tallyds.ds_vizdata VALUES
    (
        '{business_id}',
        {viztype},
        '{timestamp}',
        '{vizdata.replace("'", "''")}'
    )
    ON CONFLICT ON CONSTRAINT ds_vizdata_pkey
    DO UPDATE SET
        timestamp = excluded.timestamp,
        vizdata = excluded.vizdata
    ;
    '''
    sql
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return 0 # success
    except Exception as e:
        print(e)
        return 1 # failure


def checkVizdataTimestamp(business_id,
                          viztype,
                          days=14):
    '''check whether vizdata has been generated within a period'''
    timestamp = datetime.now() - timedelta(days=days)
    sql=f'''
    SELECT count(*)
    FROM tallyds.ds_vizdata
    WHERE business_id = '{business_id}'
    AND viztype = {viztype}
    AND timestamp >= '{timestamp.strftime('%Y-%m-%d')}'; 
    '''
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql) 
            return cursor.fetchall()[0][0]
    except Exception as e:
        print(e)
        return 0


def getLatestVizdata(business_id,
                     viztype,
                     days=14):
    timestamp = datetime.now() - timedelta(days=days)
    sql=f'''
    SELECT vizdata, 
           timestamp
    FROM tallyds.ds_vizdata
    WHERE business_id = '{business_id}'
    AND viztype = {viztype}
    AND timestamp >= '{timestamp.strftime('%Y-%m-%d')}'; 
    '''
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql) 
            # return a list of tuples
            return cursor.fetchall()
    except Exception as e:
        print(e)   
        return {}


def insertVizdataLog(business_id,
                     viztype,
                     triggeredby):
    sql=f'''
    INSERT INTO tallyds.ds_vizdata_log
    VALUES (
        uuid_generate_v4(),
        '{business_id}',
        {viztype},
        '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}',
        {triggeredby}
    );
    '''
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql) 
            return 0 # success
    except Exception as e:
        print(e)
        return 1 # failure
