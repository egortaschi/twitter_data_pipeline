import tweepy
import pandas as pd


def run_twitter_etl():

    access_key = ""
    access_secret = ""
    consumer_key = ""
    consumer_secret = ""


    # Twitter authentication
    auth = tweepy.OAuthHandler(access_key, access_secret)
    auth.set_access_token(consumer_key, consumer_secret)

    # Creating an API object
    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name='@SeattleDataGuy',
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts = False,
                            tweet_mode = 'extended'
                            )

    tweet_list = []
    for tweet in tweets:

        refined_tweet = {"user": tweet.user.screen_name,
                         # Necessary to keep full_text
                         # otherwise only the first 140 words are extracted
                         'text': tweet._json["full_text"],
                         'favorite_count': tweet.favorite_count,
                         'retweet_count': tweet.retweet_count,
                         'created_at': tweet.created_at}

        tweet_list.append(refined_tweet)

    df = pd.DataFrame(tweet_list)
    df.to_csv('refined_tweets.csv')
