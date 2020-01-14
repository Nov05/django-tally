import re
import sys
from datetime import datetime
import pandas as pd
import spacy
import scattertext as st
# Local imports
# from tallylib.scraper import yelpScraper # Deleted on 2020-01-13
from tallylib.sql import getLatestReviews

# viztype0 (Top 10 Positive/Negative Phrases)
def getReviewPosNegPhrases(df_reviews):
    if df_reviews.empty:
        return pd.DataFrame(), pd.DataFrame()

    df = df_reviews.copy()
    df['stars'] = df['stars'].astype(str)

    nlp = spacy.load("en_core_web_sm")
    nlp.Defaults.stop_words |= {'will','because','not','friends',
    'amazing','awesome','first','he','check-in',
    '=','= =','male','u','want', 'u want', 'cuz',
    'him',"i've", 'deaf','on', 'her','told','told him',
    'ins', 'check-ins','check-in','check','I', 'i"m', 
    'i', ' ', 'it', "it's", 'it.','they','coffee','place',
    'they', 'the', 'this','its', 'l','-','they','this',
    'don"t','the ', ' the', 'it', 'i"ve', 'i"m', '!', 
    '1','2','3','4', '5','6','7','8','9','0','/','.',','}

    corpus = st.CorpusFromPandas(df,
                                 category_col='stars',
                                 text_col='text',
                                 nlp=nlp).build()
    term_freq_df = corpus.get_term_freq_df()
    term_freq_df['highratingscore'] = corpus.get_scaled_f_scores('5')
    term_freq_df['poorratingscore'] = corpus.get_scaled_f_scores('1')
    dh = term_freq_df.sort_values(by='highratingscore', ascending = False)
    dh = dh[['highratingscore', 'poorratingscore']]
    dh = dh.reset_index(drop=False)
    dh = dh.rename(columns={'highratingscore': 'score'})
    dh = dh.drop(columns='poorratingscore')

    # positive dataframe, negative dataframe 
    return dh.head(10), dh.tail(10)

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
    df_reviews['date'] = pd.to_datetime(df_reviews['date'])

    # viztype0
    df_positive, df_negative = getReviewPosNegPhrases(df_reviews)
    # viztype3
    df_bydate = getYelpWordsReviewFreq(df_reviews)
 
    # API data formatting
    results = {
    'viztype0':
        {'positive': [{'term': row[0], 'score': row[1]} 
                        for row in df_positive[['term', 'score']].values], 
            'negative': [{'term': row[0], 'score': row[1]} 
                        for row in df_negative[['term', 'score']].values]
        },
    'viztype3':
        {'star_data': [{'date': row[0], 'cumulative_avg_rating': row[1], 'weekly_avg_rating': row[2]}
                        for row in df_bydate[['date_of_week', 'cumulative_avg_rating', 'stars']].values]
        }
    }
    del [df_positive, df_negative, df_bydate]

    return results