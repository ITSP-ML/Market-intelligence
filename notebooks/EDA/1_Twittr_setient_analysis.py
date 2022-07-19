# %%
# OPTIONAL: Load the "autoreload" extension so that code can change
%load_ext autoreload

# OPTIONAL: always reload modules so that as you change code in src, it gets loaded
%autoreload 2

# %%
# read data
import pandas as pd
data = pd.read_csv("data_dump/twitter_data/twiiter_data_v0.csv")
data.head()

# %%
# preprocess data
import neattext.functions as nfx
def preprocess(tweet): 
    tweet = nfx.remove_urls(tweet)  # remove urls
    tweet = nfx.remove_emails(tweet)  # remove emails
    tweet = nfx.remove_special_characters(tweet) # remove special_characters
    tweet = nfx.remove_phone_numbers(tweet) # remove phone numbers
    return tweet
data.tweet = data.tweet.apply(preprocess)
data.head()

# %%
# load model
import os
os.environ["CURL_CA_BUNDLE"] = ""  # fix ssh bug; see https://stackoverflow.com/questions/71692354/facing-ssl-error-with-huggingface-pretrained-models
from transformers import pipeline
tokenizer_kwargs = {'padding': True, 'truncation': True}
sentiment_analysis = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis", **tokenizer_kwargs)


# %%
 # generate prediction

preds = sentiment_analysis(data['tweet'].to_list())
preds_labels = [pred['label'] for pred in preds]
data['sentiment'] = preds_labels
data.head()

# %%
## save predictions 
data.to_csv("data_dump/twitter_data/sentiment_preds_v0.csv", index = False)

# %%
"""
# Load predictions
"""

# %%
# OPTIONAL: Load the "autoreload" extension so that code can change
%load_ext autoreload

# OPTIONAL: always reload modules so that as you change code in src, it gets loaded
%autoreload 2

# %%
import pandas as pd
data = pd.read_csv('data_dump/twitter_data/sentiment_preds_v0.csv')
data.head()

# %%
import pandas as pd
 
# Load the data in a dataframe
pd.set_option('display.max_colwidth', None)
 
# Show a tweet for each sentiment
display(data[data["sentiment"] == 'POS'].head(1))
display(data[data["sentiment"] == 'NEU'].head(1))
display(data[data["sentiment"] == 'NEG'].head(1))

# %%
# Let's count the number of tweets by sentiments
import matplotlib.pyplot as plt
for hashtag in data.hashtag.unique(): 
    print(f'distrubution of sentiemens for hashtag {hashtag} is')
    sentiment_counts = data[data.hashtag.eq(hashtag)].groupby(['sentiment']).size()
    print(sentiment_counts)

    # Let's visualize the sentiments
    fig = plt.figure(figsize=(6,6), dpi=100)
    ax = plt.subplot(111)
    sentiment_counts.plot.pie(ax=ax, autopct='%1.1f%%', startangle=270, fontsize=12, label="")
    plt.show()

# %%
from wordcloud import WordCloud
from wordcloud import STOPWORDS
 
# Wordcloud with positive tweets
for hashtag in data.hashtag.unique():
    positive_tweets = data[(data.hashtag.eq('casino')) & (data["sentiment"] == 'POS')].tweet
    stop_words = ["https", "co", "RT"] + list(STOPWORDS)
    positive_wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white", stopwords = stop_words).generate(str(positive_tweets))
    plt.figure()
    plt.title(f"Positive Tweets for {hashtag}- Wordcloud")
    plt.imshow(positive_wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    
    # Wordcloud with negative tweets
    negative_tweets = data[(data.hashtag.eq('casino')) & (data["sentiment"] == 'NEG')].tweet
    stop_words = ["https", "co", "RT"] + list(STOPWORDS)
    negative_wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white", stopwords = stop_words).generate(str(negative_tweets))
    plt.figure()
    plt.title(f"Negative Tweets for {hashtag} - Wordcloud")
    plt.imshow(negative_wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()



# %%
"""
**something to notice is in both hashtags negative tweets thre is the word 'NFT'**
"""

# %%
# search fo the word NFT
data[(data.tweet.str.contains('NFT') & data.sentiment.eq('NEG'))].head()

# %%
