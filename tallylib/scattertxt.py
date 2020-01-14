import re
import sys
from datetime import datetime
import pandas as pd
import spacy
import scattertext as st
import numpy as np
# Local imports
# from tallylib.scraper import yelpScraper # Deleted on 2020-01-13
from tallylib.sql import getLatestReviews

# viztype0 (Top 10 Positive/Negative Phrases)
def getReviewPosNegPhrases(df_reviews, topk=10):

    if df_reviews.empty:
        return pd.DataFrame(), pd.DataFrame()

    df = df_reviews.copy()
    df['stars'] = df['stars'].astype(str)

    nlp = spacy.load("en_core_web_sm")
    nlp.Defaults.stop_words |= {'will','because','not','friends',
    'amazing','awesome','first','he','check-in', 'and', 'some',
    '=','= =','male','u','want', 'u want', 'cuz', 'also', 'find',
    'him',"i've", 'deaf','on', 'her','told','told him',
    'ins', 'check-ins','check-in','check','I', 'i"m', 
    'i', ' ', 'it', "it's", 'it.','they','coffee','place', "it 's", "'s", 
    'they', 'the', 'this','its', 'l','-','they','this',
    'don"t','the ', ' the', 'it', 'i"ve', 'i"m', '!', '&',
    '1','2','3','4', '5','6','7','8','9','0','/','.',','}

    corpus = st.CorpusFromPandas(df,
                                 category_col='stars',
                                 text_col='text',
                                 nlp=nlp).build()
    term_freq_df = corpus.get_term_freq_df()

    categories = df['stars'].unique()
    high, poor = np.array([]), np.array([])
    if '5' in categories:
        high = corpus.get_scaled_f_scores('5')
    elif '4' in categories:
        high = corpus.get_scaled_f_scores('4')
    if '1' in categories:
        poor =  corpus.get_scaled_f_scores('1')
    elif '2' in categories:
        poor = corpus.get_scaled_f_scores('2')

    df_high, df_poor = pd.DataFrame(), pd.DataFrame()
    columns = ['term', 'score']
    if high.shape[0] > 0:
        df_high = pd.DataFrame([term_freq_df.index.tolist(), high]).T
        df_high = df_high.sort_values(1, ascending=False).head(topk)
        df_high.columns = columns
    if poor.shape[0] > 0:
        df_poor = pd.DataFrame([term_freq_df.index.tolist(), poor]).T
        df_poor = df_poor.sort_values(1, ascending=False).head(topk)
        df_poor.columns = columns

    # positive dataframe, negative dataframe 
    return df_high.head(topk), df_poor.tail(topk)

# viztype3
def getYelpWordsReviewFreq(df_reviews):
  
    if df_reviews.empty:
        return pd.DataFrame()

    df = df_reviews.copy()

    df.columns = ['date', 'text', 'stars']
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['week_number_of_year'] = df['date'].dt.week
    df = df.groupby(['year', 'month','week_number_of_year']).mean()
    df = pd.DataFrame(df.to_records()) # flatten groupby column
    df = df.iloc[::-1].head(8)
    df['cumulative_avg_rating'] = df['stars'].mean()

    # get the date of last day of the week
    list = []
    for _, row in df.iterrows():
        text = str(row['year'].astype(int)) + '-W' + \
               str(row['week_number_of_year'].astype(int)) + '-6'
        date_of_week = datetime.strptime(text, "%Y-W%W-%w").strftime('%Y-%m-%d')
        list.append(date_of_week)
    df['date_of_week'] = list
    df = df.iloc[::-1]

    return df


def getDataViztype0(business_id):
    ''' Deleted on 2020-01-13
    # do web scraping 
    yelpScraperResult = yelpScraper(business_id)
    '''
    data = getLatestReviews(business_id, limit=200)
    if len(data)==0:
        return {}
    df_reviews = pd.DataFrame(data, columns=['date', 'text', 'stars'])
    del data
    df_reviews['date'] = pd.to_datetime(df_reviews['date'])

    # viztype0
    df_positive, df_negative = getReviewPosNegPhrases(df_reviews)
    positive, negative = [], []
    if not df_positive.empty:
        positive = [{'term': row[0], 'score': row[1]} 
            for row in df_positive[['term', 'score']].values]
    if not df_negative.empty:
        negative = [{'term': row[0], 'score': row[1]} 
            for row in df_negative[['term', 'score']].values]
    viztype0 = {
        'positive': positive, 
        'negative': negative
    }
    del [df_positive, df_negative]

    # viztype3
    df_bydate = getYelpWordsReviewFreq(df_reviews)
    viztype3 = {}
    if not df_bydate.empty:
        viztype3 = {
            'star_data': [{'date': row[0], 
                           'cumulative_avg_rating': row[1], 
                           'weekly_avg_rating': row[2]}
            for row in df_bydate[['date_of_week', 'cumulative_avg_rating', 'stars']].values]
        }
    del [df_bydate]

    # API data formatting
    results = {
        'viztype0': viztype0,
        'viztype3': viztype3
        }

    return results