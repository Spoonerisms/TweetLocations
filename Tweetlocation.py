# Do "static" (i.e., not using the streaming API) geolocation search
# using code like this: d = api.search(geocode='37.781157,-122.398720,1mi')

import tweepy
from twitter_authentication import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import time

output_file = open("tweetlocations.tsv", 'w')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

# 100 is the maximum number taht can be returned according to:
# https://dev.twitter.com/rest/reference/get/search/tweets



counter = 0
for page in tweepy.Cursor(api.search, "party", geocode='47.622134,-122.320321,1mi',  count=100).pages():
    counter = counter + len(page)
    
    for tweet in page:
    #currently, this means the program will run to find tweets that contain the keyword and
    #AND associated geolocation data. when it comes across a tweet that includes party but NOT
    #geolocation data, it will return an error, 'NoneType' object is not subscriptable'. 
    #Therefore, write in an IF loop to tell the program what to do when it encounters a tweet w/o geolocation data
        lat = -1
        long = -1
        if tweet.coordinates != None:
            lat = tweet.coordinates['coordinates'][0]
            long = tweet.coordinates['coordinates'][1]
        print(tweet.user.screen_name,
            str(tweet.created_at),   
            lat, long)
    # end this loop if we've gotten 1000
    if counter == 100:
        break
print(counter)
    # This page suggests we can do one request every 5 seconds:
    # https://dev.twitter.com/rest/reference/get/search/tweets
    #time.sleep(5)


output_file.close()

#QUESTIONS
    #1. Why are we getting tweets with -1 (exact location is not specified, 
    #but tweet is still pulled?)
#http://stackoverflow.com/questions/25224692/getting-the-location-using-tweepy

#http://stackoverflow.com/questions/17633378/how-can-we-get-tweets-from-specific-country

#http://mappening.net/index.php/2013/10/twitter-api-with-python/