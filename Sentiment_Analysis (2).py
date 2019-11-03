#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Download all the required packages
import tweepy
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import re, string, unicodedata
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import csv
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from textblob import TextBlob

#Set the limit of display
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', -1)


# # Crawl Tweets

# In[ ]:


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
for tweet in tweepy.Cursor(api.search,q={"haze"},count=500, lang="en",since='').items(40000):
    message.append(tweet.text)
    user_name.append(tweet.user.name)
    created_at.append(tweet.created_at)
    location.append(tweet.user.location)
    retweet_count.append(tweet.retweet_count)
            
    #save the output to dataframe
    df=pd.DataFrame({'Message':message,'Username':user_name,'Date and Time':created_at,'Location':location,'Retweet Count':retweet_count})
    #print(df)
    
    #convert the data to csv output
    df.to_csv("Twitter Data_test2.csv")


# # Tweet Cleaning and Processing

# In[2]:


#Open the compile tweets data
haze_data=pd.read_csv(r"C:\Users\User\Desktop\UM\WQD7005\Milestone\Raw Twitter Data.csv", header='infer',sep=",")
#print(haze_data)


# In[3]:


#Create variable Sentiment Polarity
def detect_polarity(text):
    return TextBlob(text).sentiment.polarity

haze_data['Sentiment Polarity'] = haze_data['Message'].apply(detect_polarity)
#print(haze_data[1:100])


# In[4]:


#Create variable Positivity 
def pos_neg(x):
    if x>0: return 'Positive'
    elif x<0: return 'Negative'
    else: return 'Neutral'

haze_data['Positivity'] = haze_data['Sentiment Polarity'].apply(pos_neg)
print("Numbre of Positive Comment :",np.count_nonzero(haze_data['Positivity']=='Positive'))
print("Numbre of Negative Comment :",np.count_nonzero(haze_data['Positivity']=='Negative'))
print("Numbre of Neutral Comment :",np.count_nonzero(haze_data['Positivity']=='Neutral'))


# In[11]:


#Data Cleaning on the Tweets messages
for i in range(len(haze_data)):
    txt = haze_data["Message"][i]
    txt=re.sub(r"(@[A-Za-z0-9]+)|b'RT|RT|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?|^rt|https.+?|'\b\w{1,2}\b'",' ',txt)
    txt=re.sub(r'[^a-zA-Z]',' ',txt) 
    txt=re.sub(r'\b\w{1,2}\b|\d+','',txt)
    
    txt=txt.lower()
    
    stopwords = set(nltk.corpus.stopwords.words('english'))
    stopwords.update('are','and','for','its','not','mom','bulu_bulu','outsidennmom','jerebunnokay','play','bulu','https','co')
    txt = [x for x in txt.split() if x not in stopwords]
    
    stemmer = PorterStemmer()
    txt=[" ".join([stemmer.stem(word) for word in txt])]
    
    lemmatizer = WordNetLemmatizer()
    txt = [" ".join([lemmatizer.lemmatize(word) for word in txt])]
    
    haze_data.at[i,"New_Message"]=txt
    
#print(haze_data[1:100])

#Save the data as csv file
haze_data.to_csv(r"C:\Users\User\Desktop\UM\WQD7005\Milestone\Raw Twitter Data2.csv")


# In[12]:


#Split the tweets by Positivity
Positive_Comment=haze_data['New_Message'][haze_data["Positivity"]=="Positive"]
Negative_Comment=haze_data['New_Message'][haze_data["Positivity"]=="Negative"]
Neutral_Comment=haze_data['New_Message'][haze_data["Positivity"]=="Neutral"]
print(Positive_Comment[1:10])


# # Word Cloud

# In[13]:


#Create Wordcloud for every sentiment category
wordcloud1 = WordCloud(background_color="black",width = 600, height = 400).generate(str(Positive_Comment))
plt.figure()
plt.imshow(wordcloud1, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud for Positive Comment",fontsize = 20)
plt.show()

wordcloud2 = WordCloud(background_color="black",width = 600, height = 400).generate(str(Negative_Comment))
plt.figure()
plt.imshow(wordcloud2, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud for Negative Comment",fontsize = 20)
plt.show()

wordcloud3 = WordCloud(background_color="black",width = 600, height = 400).generate(str(Neutral_Comment))
plt.figure()
plt.imshow(wordcloud3, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud for Neutral Comment",fontsize = 20)
plt.show()

