#!/usr/bin/env python3

import re
import tweepy
from tweepy import OAuthHandler  # twitter
from textblob import TextBlob  # text analyser


class TwitterClient(object):
    def __init__(self):
        consumer_key = 'ENTER HERE'
        consumer_secret = 'ENTER HERE'
        access_token = 'ENTER HERE'
        access_token_secret = 'ENTER HERE'

        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Authenication Error")

    def clean_tweet(self, tweet):
        # cleans to get just the words
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=100):
        tweets = []

        try:
            fetched_tweets = self.api.search(q= query, count = count)
            for tweet in fetched_tweets:
                parsed_tweets = {}

                parsed_tweets['text'] = tweet.text
                parsed_tweets['sentiment'] = self.get_tweet_sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    if parsed_tweets not in tweets:
                        tweets.append(parsed_tweets)
                else:
                    tweets.append(parsed_tweets)

            return tweets

        except tweepy.TweepError as e:
            print(f'Error: {str(e)}')

def PosNegTweets(tweets):
    pos_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    neg_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    #neutweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']

    posTweets_percentage = 100 * (len(pos_tweets) / len(tweets))
    negTweets_percentage = 100 * (len(neg_tweets) / len(tweets))

    """print(f'''Positive Tweets = {round(posTweets_percentage,2)}% 
Negative Tweets = {round(negTweets_percentage,2)}%
Neutral Tweets = {round((100-posTweets_percentage-negTweets_percentage),2)}% ''')
    print()
    """
    return round(posTweets_percentage, 2), round(negTweets_percentage,2)


def main():
    api = TwitterClient()

    tweets = api.get_tweets(query='Bernie Sanders', count=500)
    print("Type Error")

    positive, negative = PosNegTweets(tweets)


if __name__ == "__main__":
    main()
