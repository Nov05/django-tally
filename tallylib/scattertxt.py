import pandas as pd
import spacy
import scattertext as st
import re
import sys
from datetime import datetime
# Local imports
from tallylib.scraper import yelpScraper

# spaCy imports
import en_core_web_sm
# nlp = spacy.load("en_core_web_sm/en_core_web_sm-2.2.5")
nlp = en_core_web_sm.load()


# viztype0 (Top 10 Positive/Negative Phrases)
def getReviewPosNegPhrases(yelpScraperResult):
    if yelpScraperResult.empty:
        return pd.DataFrame()

    df = yelpScraperResult.copy()

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
                                 category_col=2,
                                 text_col=1,
                                 nlp=nlp).build()

    term_freq_df = corpus.get_term_freq_df()
    term_freq_df['highratingscore'] = corpus.get_scaled_f_scores('5.0 star rating')
    term_freq_df['poorratingscore'] = corpus.get_scaled_f_scores('1.0 star rating')
    dh = term_freq_df.sort_values(by= 'highratingscore', ascending = False)
    dh = dh[['highratingscore', 'poorratingscore']]
    dh = dh.reset_index(drop=False)
    dh = dh.rename(columns={'highratingscore': 'score'})
    dh = dh.drop(columns='poorratingscore')

    # positive dataframe, negative dataframe 
    return dh.head(10), dh.tail(10)

# viztype3
def getYelpWordsReviewFreq(yelpScraperResult):
    if yelpScraperResult.empty:
        return pd.DataFrame()

    df = yelpScraperResult.copy()

    df = df.rename(columns = {0:'date', 2:'stars',1:'text'})
    df['date'] = df['date'].str.replace('\n','')
    df['date'] = df['date'].str.replace(' ','')
    df['date'] = df['date'].astype('datetime64[ns]')
    dict_rating = {'5.0 star rating':5, '4.0 star rating':4, '3.0 star rating':3, 
                  '2.0 star rating':2, '1.0 star rating':1}
    df['stars'] = df['stars'].map(dict_rating) 
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['week_number_of_year'] = df['date'].dt.week
    df = df.groupby(['year', 'month','week_number_of_year']).mean()
    df = pd.DataFrame(df.to_records()) # flatten groupby column
    df = df.iloc[::-1]
    df = df.head(8)
    df['cumulative_avg_rating'] = df['stars'].mean()

    # get the date of last day of the week
    list = []
    for _, row in df.iterrows():
        text = str(row['year'].astype(int)) + '-W' + str(row['week_number_of_year'].astype(int)) + '-6'
        date_of_week = datetime.strptime(text, "%Y-W%W-%w").strftime('%Y-%m-%d')
        list.append(date_of_week)
    df['date_of_week'] = list

    return df


def getDataViztype0(business_id):
    # do web scraping
    yelpScraperResult = yelpScraper(business_id)
    if yelpScraperResult.empty:
        return {}

    # viztype0
    df_positive, df_negative = getReviewPosNegPhrases(yelpScraperResult)
    # viztype3
    df_bydate = getYelpWordsReviewFreq(yelpScraperResult)
 
    # API data formatting
    results = {'viztype0':
                    {'positive': [{'term': pos_term, 'score': pos_score} 
                                  for pos_term, pos_score in zip(df_positive['term'], df_positive['score'])], 
                     'negative': [{'term': neg_term, 'score': neg_score} 
                                  for neg_term, neg_score in zip(df_negative['term'], df_negative['score'])]},
               'viztype3':
                    {'star_data': [{'date': row[0], 'cumulative_avg_rating': row[1], 'weekly_avg_rating': row[2]}
                                   for row in df_bydate[['date_of_week', 'cumulative_avg_rating', 'stars']].values]
                    }
              }
    del [df_positive, df_negative, df_bydate]

    return results