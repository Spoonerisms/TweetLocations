# Do "static" (i.e., not using the streaming API) geolocation search
# using code like this: d = api.search(geocode='37.781157,-122.398720,1mi')

import tweepy
from twitter_authentication import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import time


ts = time.time()
output_file = open('tweetlocationRays_' + str(ts) + '.tsv','w')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

# 100 is the maximum number that can be returned according to:
# https://dev.twitter.com/rest/reference/get/search/tweets

def get_tweets_for_keyword(keyword):
    counter = 0
    for page in tweepy.Cursor(api.search, keyword,  geocode='27.768225,-82.653392,100mi',  count=100).pages():
        counter = counter + len(page)
        
        for tweet in page:
        #currently, this means the program will run to find tweets that contain the keyword and
        #AND associated geolocation data. when it comes across a tweet that includes party but NOT
        #geolocation data, it will return an error, 'NoneType' object is not subscriptable'. 
        #Therefore, write in an IF loop to tell the program what to do when it encounters a tweet w/o geolocation data
            lat = -1
            long = -1
            
            user_name   = tweet.user.screen_name
            text        = ' '.join(tweet.text.split())
            #Had to filter out tweets with the following characters
            text        = text.translate('"<>{}|')

            

            if tweet.coordinates != None:
                lat = tweet.coordinates['coordinates'][1]
                long = tweet.coordinates['coordinates'][0]
                
            
#             output_file.write("User Name: " + tweet.user.screen_name + '\n')
#             output_file.write("Text: "  + (tweet.text) + '\n')
             
#             
#             
#             output_file.write("Date: " + date[0] + '\n')
#             output_file.write("Time: " + date[1] + '\n')
#             output_file.write("Lat : " + str(lat) + '\n')
#             output_file.write("Long : "+ str(long) + '\n\n')
    
      #Had to split time and date
            date = str(tweet.created_at).split(' ')
            output = user_name + '\t' + text + '\t' + date[0] + '\t' + date[1] + '\t' 
            output += str(lat) + '\t' + str(long) + '\n'
            
            if tweet.id not in tweet_ids:       
                 output_file.write(output)
                 tweet_ids.append(tweet.id)
                            
        # end this loop if we've gotten 1000
        if counter == 500:
            break
        
    print(counter)
    # This page suggests we can do one request every 5 seconds:
    # https://dev.twitter.com/rest/reference/get/search/tweets
    #time.sleep(5)

tweet_ids = []

get_tweets_for_keyword("Mariners")
get_tweets_for_keyword("'#Mariners'")
get_tweets_for_keyword("Rays")
get_tweets_for_keyword("baseball")

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
#git -m "message" 
#git push

