# %%


# OPTIONAL: Load the "autoreload" extension so that code can change
%load_ext autoreload

# OPTIONAL: always reload modules so that as you change code in src, it gets loaded
%autoreload 2

# %%
import tweepy
import os
os.environ["CURL_CA_BUNDLE"] = ""  # fix ssh bug; see https://stackoverflow.com/questions/71692354/facing-ssl-error-with-huggingface-pretrained-models
# Add Twitter API key and secret
api_key= "oezoysDKsVMI8N1VYfCij0jhA"
api_secret= "gJpiBhMiHvOmPKLN1lDWQAWH8pOx3peF4LFiiIhBOV1h7ZlGMf"
consumer_key = "716362565-lbMoiG9hfu6lDQuAYlVp7LwDM16epL8kYBy8cqhQ"
consumer_secret = "F3xoORbXP5qQzTbffnyEEwwynfYlENk7BNpqLOyZIHHQC"

# Handling authentication with Twitter

auth = tweepy.OAuth1UserHandler(
   api_key, api_secret, consumer_key, consumer_secret
)
# Create a wrapper for the Twitter API
api = tweepy.API(auth, wait_on_rate_limit=True)



# %%
# Helper function for handling pagination in our search and handle rate limits
import  time
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print('Reached rate limite. Sleeping for >15 minutes')
            time.sleep(15 * 61)
        except StopIteration:
            break

def get_tweets(hashtag): 
    # Define the term we will be using for searching tweets
    query = '#'+ hashtag
    query = query + ' -filter:retweets'

    # Define how many tweets to get from the Twitter API 
    count = 1000

    # Let's search for tweets using Tweepy 
    search = limit_handled(tweepy.Cursor(api.search_tweets,
                            q=query,
                            tweet_mode='extended',
                            lang='en',
                            result_type="recent").items(count))
    return search 

# %%
"""
# create tweets dataset
"""

# %%
## geberate empty data frame 
import pandas as pd
data = pd.DataFrame(columns=["hashtag", "tweet"])


# %%
# Let's run the sentiment analysis on each tweet
hashtags = ['sportsbook', 'casino']
for hashtag in hashtags:
  search = get_tweets(hashtag)
  for tweet in search:
      try: 
        content = tweet.full_text
        row = {'hashtag':hashtag, 'tweet': content}
        data.loc[len(data)] = [hashtag, content]
        # data = pd.concat([data,row])

      except: 
        pass

# %%
# show data
data.head()

# %%
## save data
data.to_csv('data_dump/twitter_data/twiiter_data_v0.csv', index=False)

# %%
