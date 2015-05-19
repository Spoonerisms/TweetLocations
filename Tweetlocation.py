# Do "static" (i.e., not using the streaming API) geolocation search
# using code like this: d = api.search(geocode='37.781157,-122.398720,1mi')

import tweepy
from twitter_authentication import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import time

ts = time.time()
output_file = open('tweetlocation_' + str(ts) + '.tsv','w')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

# 100 is the maximum number that can be returned according to:
# https://dev.twitter.com/rest/reference/get/search/tweets



def get_tweets_for_keyword(keyword):
    counter = 0
    for page in tweepy.Cursor(api.search, keyword,  geocode='47.622134,-122.320321,5mi',  count=100).pages():
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
            output_file.write(tweet.user.screen_name + "\t" + (tweet.text) + "\t" + str(tweet.created_at) + "\t" + str(lat) + "\t" + str(long))
    
        # end this loop if we've gotten 1000
        if counter == 500:
            break
        
    print(counter)
    # This page suggests we can do one request every 5 seconds:
    # https://dev.twitter.com/rest/reference/get/search/tweets
    #time.sleep(5)

get_tweets_for_keyword("game")
get_tweets_for_keyword("mariners")

output_file.close()

#QUESTIONS
#Having issue converting lat/lon to string. need to convert lat/lon to string in order to print information in crontab
#runs by hand but not with cron tab (tweetlocation.txt is remains blank. error when running has something to do with unicode on lat/lon value? horizontal elipses? see screenshot) 

    #1. Why are we getting tweets with -1 (exact location is not specified, 
    #but tweet is still pulled?)
#http://stackoverflow.com/questions/25224692/getting-the-location-using-tweepy

#http://stackoverflow.com/questions/17633378/how-can-we-get-tweets-from-specific-country

#http://mappening.net/index.php/2013/10/twitter-api-with-python/

# git add "whatever file name is"
#git commit -m "message" 
#git push

