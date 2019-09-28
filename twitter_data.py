#!/usr/bin/env python
# coding: utf-8

# In[14]:


import tweepy
import csv
import pandas as pd
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

####input your credentials here
consumer_key = 'JWhVdjJL5A9HBYhFhXji8Gui4'
consumer_secret = 'yKcZZnozSl9WZuy96UJUFfpc7tAl36NtQP80AOlYYAjTjizEaX'
access_token = '1177240797592244224-9IsJd12zTyw2PEZ1MNzdQO9Ul1aUBy'
access_token_secret = '0JHYUksBBpkOiV5lwmVRft55ERyeikpapSgOcuDeUM1UD'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


# Open/Create a file to append data
csvFile = open('ua.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)

message,favorite_count,retweet_count,created_at,user_name,favourites_count,location=[],[],[],[],[],[],[]

for tweet in tweepy.Cursor(api.search,q={"haze,jerebu"},count=1000,
                           lang="en",
                           since="2019-01-01").items():
    #print (tweet.created_at,tweet.place,tweet.text)
    #csvWriter.writerow([tweet.created_at,tweet.place,tweet.text.encode('utf-8')])
    message.append(tweet.text)
    favorite_count.append(tweet.favorite_count)
    retweet_count.append(tweet.retweet_count)
    created_at.append(tweet.created_at)
    user_name.append(tweet.user.name)
    favourites_count.append(tweet.user.favourites_count)
    location.append(tweet.user.location)
 
    df=pd.DataFrame({'Message':message,
                'Tweet Favorite Count':favorite_count,
                'Retweet Count':retweet_count,
                'Created At':created_at,
                'Username':user_name,
                'Likes':favourites_count,
                'Location':location})
    
    df.to_csv("Twitter Data.csv")
    print(df)


# In[16]:


to script twitter_data.ipynb


# In[ ]:




