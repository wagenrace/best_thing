import json
import os
import time

import pandas as pd
import tweepy

with open("keys.json", "r") as f:
    keys = json.load(f)

auth = tweepy.OAuthHandler(keys["ConsumerKey"], keys["ConsumerKeySecret"])
auth.set_access_token(keys["AccessToken"], keys["AccessTokenSecret"])

# Create API object
api = tweepy.API(auth)

search_words = 'is AND better AND then'
numTweets = 100
db_tweets = pd.DataFrame(columns = ['username', 'acctdesc', 'location', 'following',
                                        'followers', 'totaltweets', 'usercreatedts', 'tweetcreatedts',
                                        'retweetcount', 'text', 'hashtags'])
                            
tweets = tweepy.Cursor(api.search_tweets, q=search_words, lang="en", tweet_mode='extended').items(numTweets)
# Store these tweets into a python list
tweet_list = [tweet for tweet in tweets]
# Obtain the following info (methods to call them out):
# user.screen_name - twitter handle
# user.description - description of account
# user.location - where is he tweeting from
# user.friends_count - no. of other users that user is following (following)
# user.followers_count - no. of other users who are following this user (followers)
# user.statuses_count - total tweets by user
# user.created_at - when the user account was created
# created_at - when the tweet was created
# retweet_count - no. of retweets
# (deprecated) user.favourites_count - probably total no. of tweets that is favourited by user
# retweeted_status.full_text - full text of the tweet
# tweet.entities['hashtags'] - hashtags in the tweet
# Begin scraping the tweets individually:
noTweets = 0
for tweet in tweet_list:
# Pull the values
    username = tweet.user.screen_name
    acctdesc = tweet.user.description
    location = tweet.user.location
    following = tweet.user.friends_count
    followers = tweet.user.followers_count
    totaltweets = tweet.user.statuses_count
    usercreatedts = tweet.user.created_at
    tweetcreatedts = tweet.created_at
    retweetcount = tweet.retweet_count
    hashtags = tweet.entities['hashtags']
    try:
        text = tweet.retweeted_status.full_text
    except AttributeError:  # Not a Retweet
        text = tweet.full_text
# Add the 11 variables to the empty list - ith_tweet:
    ith_tweet = [username, acctdesc, location, following, followers, totaltweets,
                    usercreatedts, tweetcreatedts, retweetcount, text, hashtags]
# Append to dataframe - db_tweets
    db_tweets.loc[len(db_tweets)] = ith_tweet
# increase counter - noTweets  
    noTweets += 1