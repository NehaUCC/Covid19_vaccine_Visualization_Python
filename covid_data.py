import tweepy
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import tweepy as tw # To extarct the twitter data
from tqdm import tqdm

api_key ='dCtSqtHBRCCvqy5sMntgTe479'
api_secret_key ='0KbXy4xqwiXDxzL6H8kYdV61D9NJJwzdixOUReAodHN73N1Mm0'
access_token ='471823308-bbyGGnuWNGIfkdzGEHnzDNBhUoyB2RxPdqr0W5DB'
access_token_secret ='SeHJpAURHBeoFq8yATKsvtI8vpkJl4kJiySfEVFF7syL9'
auth = tw.OAuthHandler(api_key, api_secret_key)
api = tw.API(auth, wait_on_rate_limit=True)

search_words = "#Udemy -filter:retweets" #Type you keywork here instead of #covidvaccine
#You can fix a time frame with the date since and date until parameters
date_since = "2021-03-01"
#date_since = "2021-04-01"
date_until="2021-04-06"
# Collect tweets
tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since,
              until=date_until     
              ).items(7500)
tweets_copy = []
for tweet in tqdm(tweets):
    tweets_copy.append(tweet)

print(f"New tweets retrieved: {len(tweets_copy)}")

tweets_df = pd.DataFrame()
for tweet in tqdm(tweets_copy):
    hashtags = []
    try:
        for hashtag in tweet.entities["hashtags"]:
            hashtags.append(hashtag["text"])
    except:
        pass
    tweets_df = tweets_df.append(pd.DataFrame({'user_name': tweet.user.name, 
                                               'user_location': tweet.user.location,\
                                               'user_description': tweet.user.description,
                                               'user_created': tweet.user.created_at,
                                               'user_followers': tweet.user.followers_count,
                                               'user_friends': tweet.user.friends_count,
                                               'user_favourites': tweet.user.favourites_count,
                                               'user_verified': tweet.user.verified,
                                               'date': tweet.created_at,
                                               'text': tweet.text, 
                                               'hashtags': [hashtags if hashtags else None],
                                               'source': tweet.source,
                                               'is_retweet': tweet.retweeted}, index=[0]))
        
tweets_df
tweets_df.to_csv('C:/Users/nthak/OneDrive/Desktop/Udemy.csv', index=False)





