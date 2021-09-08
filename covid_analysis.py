# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 08:27:50 2021

@author: nthak
"""

from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np 
import pandas as pd
#import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob 
from wordcloud import WordCloud, STOPWORDS
import warnings
warnings.simplefilter("ignore")

#tweets_df = pd.read_csv("C:/Users/nthak/OneDrive/Desktop/vaccination_all_tweets.csv")
tweets_df = pd.read_csv("C:/Users/nthak/OneDrive/Desktop/Pfizer_Moderna_final.csv")
print(f"data shape: {tweets_df.shape}")
tweets_df.info()
def plot_count(feature, title, df, size=1, ordered=True):
    f, ax = plt.subplots(1,1, figsize=(4*size,4))
    total = float(len(df))
    if ordered:
        g = sns.countplot(df[feature], order = df[feature].value_counts().index[:20], palette='Set3')
    else:
        g = sns.countplot(df[feature], palette='Set3')
    g.set_title("Number and percentage of {}".format(title))
    if(size > 2):
        plt.xticks(rotation=90, size=8)
    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x()+p.get_width()/2.,
                height,
                '{:1.2f}%'.format(100*height/total),
                ha="center") 
    plt.show()    
#plot_count("user_name", "User name", tweets_df,4)
plot_count("user_location", "User location", tweets_df,4)
plot_count("source", "Source", tweets_df,4)
plot_count("hashtags", "Hashtags", tweets_df, 4)

#--------------------------------------------------------------- Wordcloud
from wordcloud import WordCloud, STOPWORDS
def show_wordcloud(data, title=""):
    text = " ".join(t for t in data.dropna())
    stopwords = set(STOPWORDS)
    stopwords.update(["t", "co", "https", "amp", "U"])
    wordcloud = WordCloud(stopwords=stopwords, scale=4, max_font_size=40, max_words=400,background_color="white").generate(text)
    fig = plt.figure(1, figsize=(16,16))
    plt.axis('off')
    fig.suptitle(title, fontsize=30)
    fig.subplots_adjust(top=2.3)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.show()
show_wordcloud(tweets_df['text'], title = 'Widely used words in tweets')
#-------------------------------------------------------------------------------Sentiment Analysis

sia = SentimentIntensityAnalyzer()
def find_sentiment(post):
    if sia.polarity_scores(post)["compound"] > 0:
        return "Positive"
    elif sia.polarity_scores(post)["compound"] < 0:
        return "Negative"
    else:
        return "Neutral"

def plot_sentiment(df, feature, title):
    counts = df[feature].value_counts()
    percent = counts/sum(counts)

    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 5))

    counts.plot(kind='bar', ax=ax1, color='purple')
    percent.plot(kind='bar', ax=ax2, color='pink')
    ax1.set_ylabel(f'Counts : {title} sentiments', size=12)
    ax2.set_ylabel(f'Percentage : {title} sentiments', size=12)
    #plt.suptitle(f"Sentiment analysis: {title}")
    plt.tight_layout()
    plt.show()
tweets_df['sentiment'] = tweets_df['text'].apply(lambda x: find_sentiment(x))
plot_sentiment(tweets_df, 'sentiment', 'Text')













