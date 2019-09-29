## Tweet Scraping 

#Import the necessary packages
import tweepy
import csv
import pandas as pd
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

#adjust the output display screen size
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

#input credentials here
consumer_key = 'JWhVdjJL5A9HBYhFhXji8Gui4'
consumer_secret = 'yKcZZnozSl9WZuy96UJUFfpc7tAl36NtQP80AOlYYAjTjizEaX'
access_token = '1177240797592244224-9IsJd12zTyw2PEZ1MNzdQO9Ul1aUBy'
access_token_secret = '0JHYUksBBpkOiV5lwmVRft55ERyeikpapSgOcuDeUM1UD'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

#Extract the data required and put them into list
message,user_name,created_at,location,retweet_count=[],[],[],[],[]

#input the words would like to find in the query search 'q={}'
#input number of tweets in 'items()' would like to run
for tweet in tweepy.Cursor(api.search,q={"haze,jerebu"},count=500, lang="en").items(10000):
    
    message.append(tweet.text)
    user_name.append(tweet.user.name)
    created_at.append(tweet.created_at)
    location.append(tweet.user.location)
    retweet_count.append(tweet.retweet_count)

    #save the output to dataframe
    df=pd.DataFrame({'Message':message,'Username':user_name,'Date and Time':created_at,'Location':location,'Retweet Count':retweet_count})
    print(df)
    
    #convert the data to csv output
    df.to_csv("Twitter Data.csv")
