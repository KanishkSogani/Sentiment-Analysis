import re
import json
from flask import Flask, request, jsonify
from nltk.corpus import stopwords
import tensorflow as tf
from keras.utils import pad_sequences
import pandas as pd
import keras
import nltk
import collections
import numpy as np
import pandas as pd
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib import rcParams
from wordcloud import WordCloud, STOPWORDS
import os
import matplotlib
import tensorflow_hub as hub
import tensorflow_text as text
import csv
from getpass import getpass
from time import sleep 
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
#from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import wait
from selenium.webdriver.support.ui import WebDriverWait
import itertools
from bs4 import BeautifulSoup
import requests
import googleapiclient
from googleapiclient import discovery
from googleapiclient import errors
import asyncpraw 
from asyncpraw.models import MoreComments
model = tf.keras.models.load_model("kirtan_glove_twitter_raddit")

app = Flask(__name__)

#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importing the necessary libraries


# In[2]:

reddit = asyncpraw.Reddit(user_agent="Comment Extraction (by /u/heerak_ts08)",
                     client_id="", 
                     client_secret="")

async def reddit_comments(x):
    url = x
    submission = await reddit.submission(url = url)
    comments = await submission.comments()
    posts = []
    for top_level_comment in comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        #print(top_level_comment.body)
        posts.append(top_level_comment.body)
    posts = pd.DataFrame(posts,columns=["text"])
    return posts

def get_yt_data(x):
    try:
        y = x.split('=')
        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = "AIzaSyAAW71vtCeQRiqirxS_GjAnjYkzdZFgig8"

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey = DEVELOPER_KEY)

        request = youtube.commentThreads().list(
            part = "snippet",
            videoId = y[1],
            maxResults = 100
        )
        response = request.execute()
        comments = []
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append([
                comment['authorDisplayName'],
                comment['publishedAt'],
                comment['updatedAt'],
                comment['likeCount'],
                comment['textDisplay']
            ])
        df = pd.DataFrame(comments, columns=['author', 'published_at', 'updated_at', 'like_count', 'text'])
        return df
    except Exception as e:
        print(e)




def get_tweet_data(card):
    """Extract data from tweet card"""
    try:
        postdate = card.find_element(By.XPATH,'.//time').get_attribute('datetime')
    except NoSuchElementException:
        return
    
    comment = card.find_element(By.XPATH,'.//div[2]/div[2]/div[1]').text
    responding = card.find_element(By.XPATH,'.//div[2]/div[2]/div[2]').text
    text = comment + responding
    reply_cnt = card.find_element(By.XPATH,'.//div[@data-testid="reply"]').text
    retweet_cnt = card.find_element(By.XPATH,'.//div[@data-testid="retweet"]').text
    like_cnt = card.find_element(By.XPATH,'.//div[@data-testid="like"]').text
    tweet = (postdate, text, reply_cnt, retweet_cnt, like_cnt)
    return tweet


# In[3]:


#setting the driver
# driver = Chrome()
# driver.get("https://www.twitter.com/login")


# # In[4]:


# #entering the email
# wait = WebDriverWait(driver, 10)
# wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="text"]'))).send_keys("mark85ha08@gmail.com")
# wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(.,'Next')]"))).click()


# # In[5]:


# #entering the username
# #wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="text"]'))).send_keys("@hero_agraw50737")
# #wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(.,'Next')]"))).click()


# # In[6]:


# #entering the password
# wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="password"]'))).send_keys("@Sahha08")
# wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(.,'Log in')]"))).click()


# # In[7]:


# #reaching the user_id's page
# # x = str(input("enter the user id(without @): "))
# # driver.get("https://www.twitter.com/" + x)


# # In[8]:


# #reach the posts section
# #wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Posts"))).click()


# # In[9]:


# #creating the list of posts
#wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Posts"))).click()
#new_cards = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))
#new_card = new_cards[2]
#get_tweet_data(new_card)



# In[10]:


#to get all you tweets reach
def get_all_tweets_data(x):
    driver = Chrome()
    driver.get("https://www.twitter.com/login")
    wait = WebDriverWait(driver, 10)
    # wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="text"]'))).send_keys("mark85ha08@gmail.com")
    # wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(.,'Next')]"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="text"]'))).send_keys("@HeerakA1000")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(.,'Next')]"))).click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="password"]'))).send_keys("")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(.,'Log in')]"))).click()

    #x = str(input("enter the user id(without @): "))
    driver.get("https://www.twitter.com/" + x)
    # wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="text"]'))).send_keys("@HeroAgraw5073")
    # wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(.,'Next')]"))).click()

    # wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="password"]'))).send_keys("")
    # wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(.,'Log in')]"))).click()
    sleep(5)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Posts"))).click()
    data = []
    tweet_ids = set()
    last_position = driver.execute_script("return window.pageYOffset;")
    scrolling = True

    while scrolling:
        page_cards = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))
        for card in page_cards[-15:]:
            tweet = get_tweet_data(card)
            if tweet:
                tweet_id = ''.join(tweet)
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    data.append(tweet)

        scroll_attempt = 0
        while True:
            # check scroll position
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(2)
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1

                # end of scroll region
                if scroll_attempt >= 3:
                    scrolling = False
                    break
                else:
                    sleep(2) # attempt another scroll
            else:
                last_position = curr_position
                break 
    df = pd.DataFrame(data, columns = ["date and time", "text", "reply_count", "retweet_count", "like_count"])
    return df

# In[ ]:





# In[16]:


#to get the replies of the first post
#wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Posts"))).click()
#wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="tweet"]'))).click()
#page_replies = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))
#page_replies[0].text()
#page_reply = page_replies[1]
#page_reply.text
#page_reply = page_replies[2]
#print(page_reply.text)


# In[ ]:





# In[12]:


# wait = WebDriverWait(driver, 10)
# wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Posts"))).click()
# tweets = []
# result = False
# old_height = driver.execute_script("return document.body.scrollHeight")

# #set initial all_tweets to start loop
# all_tweets = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))

# while result == False:

#     for item in all_tweets[1:]: # skip tweet already scrapped

#         print('--- date ---')
#         try:
#             date = item.find_element(By.XPATH, './/time').text
#         except:
#             date = '[empty]'
#         print(date)

#         print('--- text ---')
#         try:
#             text = item.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
#         except:
#             text = '[empty]'
#         print(text)

#         print('--- replying_to ---')
#         try:
#             replying_to = item.find_element(By.XPATH,'.//div[@data-testid="cellInnerDiv"]' ).text
#         except:
#             replying_to = '[empty]'
#         print(replying_to)
    
#         #Append new tweets replies to tweet array
#         tweets.append([date, replying_to, text])
    
#     #scroll down the page
#     driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

#     sleep(2)
    
#     try:
#         try:
#             button = driver.find_element_by_css_selector("div.css-901oao.r-1cvl2hr.r-37j5jr.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-q4m81j.r-qvutc0")
#         except:
#             button = driver.find_element_by_css_selector("div.css-1dbjc4n.r-1ndi9ce") #there are two kinds of buttons
        
#         ActionChains(driver).move_to_element(button).click(button).perform()
#         sleep(2)
#         driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
#         sleep(2)
#     except:
#         pass

#     new_height = driver.execute_script("return document.body.scrollHeight")

#     if new_height == old_height:
#         result = True
#     old_height = new_height

#     #update all_tweets to keep loop
#     all_tweets = driver.find_elements(By.XPATH, '//div[@data-testid]//article[@data-testid="tweet"]')

# tweets = tweets.sort()
# tweets = list(k for k in itertools.groupby(tweets) or []) #remove duplicates from final list
# tweets


# In[ ]:






def predict_function_bert(text):
    
    data=pd.DataFrame()
    data["text"]=text    
    TAG_RE = re.compile(r'<[^>]+>')
    
    def remove_tags(text):
        return TAG_RE.sub('', text)
    

    
    def preprocess_text(sen):
        
        sentence = sen.lower()

    # Remove html tags
        sentence = remove_tags(sentence)

    # Remove punctuations and numbers
        sentence = re.sub('[^a-zA-Z]', ' ', sentence)

    # Single character removal
        sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)  # When we remove apostrophe from the word "Mark's", the apostrophe is replaced by an empty space. Hence, we are left with single character "s" that we are removing here.

    # Remove multiple spaces
        sentence = re.sub(r'\s+', ' ', sentence)  # Next, we remove all the single characters and replace it by a space which creates multiple spaces in our text. Finally, we remove the multiple spaces from our text as well.

    # Remove Stopwords
        pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
        sentence = pattern.sub('', sentence)

        return sentence
    
    X= []
    sentences = list(data['text'])
    for sen in sentences:
        X.append(preprocess_text(sen))
    
    x=np.array(X)
    # os.environ['TFHUB_CACHE_DIR'] = os.path.expanduser('~/.cache/tfhub_modules')
    os.environ['TFHUB_CACHE_DIR'] = os.path.expanduser('~/.cache/tfhub_modules')
    new_model_kaggle=keras.models.load_model("kirtan_bert_twitter_radit.h5",custom_objects={'KerasLayer':hub.KerasLayer},compile=False)
    new_model_kaggle.compile()
    fin = new_model_kaggle.predict(x)
    # fin = fin.flatten()
    # my_list = fin.tolist()
    # json_data = json.dumps(my_list)
    # return json_data
    input_array=fin
    binary_array = np.zeros_like(input_array)
    max_indices = np.argmax(input_array, axis=1)
    binary_array[np.arange(len(input_array)), max_indices] = 1
    y=[]
    a,b,c=int(0),int(0),int(0)

    for i in binary_array:
        if(np.array_equal(i,[1., 0., 0.])):
            y.append("Neutral")
            a+=1    
        if(np.array_equal(i,[0., 1., 0.])):
            y.append("Positive")
            b+=1         
        if(np.array_equal(i,[0., 0., 1.])):
            y.append("Negative")
            c+=1


    sum=a+b+c
    nut_per=round((a*100)/sum,2)
    pos_per=round((b*100)/sum,2)
    neg_per=round((c*100)/sum,2)
    percentage=[nut_per,pos_per,neg_per]
    percentage_json=json.dumps(percentage)
    data["sentiment"]=y 
    json_bert_pred = data.to_json(orient ='records')
    return json_bert_pred,percentage_json
    
def predict_function(text):

    data = pd.DataFrame()
    data["text"] = text
    # data["text"].dropna(inplace=True)
    TAG_RE = re.compile(r'<[^>]+>')

    def remove_tags(text):
        return TAG_RE.sub('', text)

    nltk.download('stopwords')

    def preprocess_text(sen):
        sen = sen[0]
        sentence = sen.lower()

    # Remove html tags
        sentence = remove_tags(sentence)

    # Remove punctuations and numbers
        sentence = re.sub('[^a-zA-Z]', ' ', sentence)

    # Single character removal
        # When we remove apostrophe from the word "Mark's", the apostrophe is replaced by an empty space. Hence, we are left with single character "s" that we are removing here.
        sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)

    # Remove multiple spaces
        # Next, we remove all the single characters and replace it by a space which creates multiple spaces in our text. Finally, we remove the multiple spaces from our text as well.
        sentence = re.sub(r'\s+', ' ', sentence)

    # Remove Stopwords
        pattern = re.compile(
            r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
        sentence = pattern.sub('', sentence)

        return sentence

    X = []
    sentences = list(data['text'])
    for sen in sentences:
        X.append(preprocess_text(sen))
    x = X
    import joblib
    mt = joblib.load("tokenize_glove_twitter_raddit")
    x_tokinized = mt.texts_to_sequences(x)
    x_padded = pad_sequences(x_tokinized, padding='post', maxlen=50)
    fin = model.predict(x_padded)
    # fin = fin.flatten()
    my_list = fin.tolist()
    json_data = json.dumps(my_list)
    return json_data


def predict_function_bert_comment_static():
    data_initial=pd.read_csv("Twitter_Data.csv")
    data=pd.DataFrame()
    data["text"]=data_initial['clean_text'].iloc[152969:153969]
    data.dropna(inplace=True)
    TAG_RE = re.compile(r'<[^>]+>')

    def remove_tags(text):
        return TAG_RE.sub('', text)
    

    
    def preprocess_text(sen):
        
        sentence = sen.lower()

    # Remove html tags
        sentence = remove_tags(sentence)

    # Remove punctuations and numbers
        sentence = re.sub('[^a-zA-Z]', ' ', sentence)

    # Single character removal
        sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)  # When we remove apostrophe from the word "Mark's", the apostrophe is replaced by an empty space. Hence, we are left with single character "s" that we are removing here.

    # Remove multiple spaces
        sentence = re.sub(r'\s+', ' ', sentence)  # Next, we remove all the single characters and replace it by a space which creates multiple spaces in our text. Finally, we remove the multiple spaces from our text as well.

    # Remove Stopwords
        pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
        sentence = pattern.sub('', sentence)

        return sentence
    
    X= []
    sentences = list(data['text'])
    for sen in sentences:
        X.append(preprocess_text(sen))

    x=np.array(X)
    os.environ['TFHUB_CACHE_DIR'] = os.path.expanduser('~/.cache/tfhub_modules')
    new_model_kaggle=keras.models.load_model("kirtan_bert_twitter_radit.h5",custom_objects={'KerasLayer':hub.KerasLayer},compile=False)
    new_model_kaggle.compile()
    predict=new_model_kaggle.predict(x)
    input_array=predict
    binary_array = np.zeros_like(input_array)
    max_indices = np.argmax(input_array, axis=1)
    binary_array[np.arange(len(input_array)), max_indices] = 1
    y=[]
    a,b,c=int(0),int(0),int(0)

    for i in binary_array:
        if(np.array_equal(i,[1., 0., 0.])):
            y.append("Neutral")
            a+=1    
        if(np.array_equal(i,[0., 1., 0.])):
            y.append("Positive")
            b+=1         
        if(np.array_equal(i,[0., 0., 1.])):
            y.append("Negative")
            c+=1


    sum=a+b+c
    nut_per=round((a*100)/sum,2)
    pos_per=round((b*100)/sum,2)
    neg_per=round((c*100)/sum,2)
    percentage=[nut_per,pos_per,neg_per]
    percentage_json=json.dumps(percentage)
    data["sentiment"]=y 
    json_bert_pred = data.to_json(orient ='records')
    return json_bert_pred,percentage_json

def predict_function_excel_file(name):
    data_initial=pd.read_csv(name)
    data=pd.DataFrame()
    data["text"]= data_initial["Text"]
    TAG_RE = re.compile(r'<[^>]+>')
    def remove_tags(text):
        return TAG_RE.sub('', text)
    

    
    def preprocess_text(sen):
        
        sentence = sen.lower()

    # Remove html tags
        sentence = remove_tags(sentence)

    # Remove punctuations and numbers
        sentence = re.sub('[^a-zA-Z]', ' ', sentence)

    # Single character removal
        sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)  # When we remove apostrophe from the word "Mark's", the apostrophe is replaced by an empty space. Hence, we are left with single character "s" that we are removing here.

    # Remove multiple spaces
        sentence = re.sub(r'\s+', ' ', sentence)  # Next, we remove all the single characters and replace it by a space which creates multiple spaces in our text. Finally, we remove the multiple spaces from our text as well.

    # Remove Stopwords
        pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
        sentence = pattern.sub('', sentence)

        return sentence
    
    X= []
    sentences = list(data['text'])
    for sen in sentences:
        X.append(preprocess_text(sen))
    
    x=np.array(X)
    os.environ['TFHUB_CACHE_DIR'] = os.path.expanduser('~/.cache/tfhub_modules')
    new_model_kaggle=keras.models.load_model("kirtan_bert_twitter_radit.h5",custom_objects={'KerasLayer':hub.KerasLayer},compile=False)
    new_model_kaggle.compile()
    predict=new_model_kaggle.predict(x)
    input_array=predict
    binary_array = np.zeros_like(input_array)
    max_indices = np.argmax(input_array, axis=1)
    binary_array[np.arange(len(input_array)), max_indices] = 1
    y=[]
    a,b,c=int(0),int(0),int(0)

    for i in binary_array:
        if(np.array_equal(i,[1., 0., 0.])):
            y.append("Neutral")
            a+=1    
        if(np.array_equal(i,[0., 1., 0.])):
            y.append("Positive")
            b+=1         
        if(np.array_equal(i,[0., 0., 1.])):
            y.append("Negative")
            c+=1


    sum=a+b+c
    nut_per=round((a*100)/sum,2)
    pos_per=round((b*100)/sum,2)
    neg_per=round((c*100)/sum,2)
    percentage=[nut_per,pos_per,neg_per]
    percentage_json=json.dumps(percentage)
    data["sentiment"]=y 
    json_bert_pred = data.to_json(orient ='records')
    return json_bert_pred,percentage_json

def word_cloud(text):
    matplotlib.use('agg')
    data_word_cloud=pd.DataFrame()
    data_word_cloud["text"]=text
    text=list(data_word_cloud["text"])
    text=" ".join(review for review in text)
    stopwords = STOPWORDS
    wordcloud = WordCloud(stopwords=stopwords, background_color="#fcfcfa", max_words=50,margin=5 ,width=800, height=400).generate(text)
    rcParams['figure.figsize'] = 20,20
    plt.imshow(wordcloud)
    plt.axis("off")
    path = os.path.join(os.path.expanduser("~"), 'C:/Users/prabh/OneDrive/Desktop/SIH/SIH-Ground1/SIH-Ground/public/Resources/')
    file_name = "my_word_cloud.png"
    file_path = os.path.join(path, file_name)
    plt.savefig(file_path, transparent = True)
    return

def word_cloud_comment_static():
    data_initial=pd.read_csv("Twitter_Data.csv")
    data=pd.DataFrame()
    data["text"]=data_initial['clean_text'].iloc[152969:153969]
    data.dropna(inplace=True)
    text=data["text"]
    text=" ".join(review for review in text)
    stopwords = STOPWORDS
#    wordcloud = WordCloud(stopwords=stopwords, background_color=None, max_words=50,margin=5,mode="RGBA").generate(text)
    #FF0000
    wordcloud = WordCloud(stopwords=stopwords, background_color='#fcfcfa', max_words=50,margin=5,).generate(text)
    rcParams['figure.figsize'] = 20,20
    plt.imshow(wordcloud)
    plt.axis("off")
    desktop_path = os.path.join(os.path.expanduser("~"), 'C:/Users/prabh/OneDrive/Desktop/SIH/SIH-Ground1/SIH-Ground/public/Resources/')
    file_name1 = "my_word_cloud1.png"
    file_path1 = os.path.join(desktop_path, file_name1)
    plt.savefig(file_path1, transparent = True)
    return

def world_cloud_excel_file(file_name):
    data_initial=pd.read_csv(file_name)
    data_initial.dropna(inplace=True)
    data=pd.DataFrame()
    data["text"]= data_initial["Text"]
    text=data['text']
    text=" ".join(review for review in text)
    stopwords = STOPWORDS
#    wordcloud = WordCloud(stopwords=stopwords, background_color=None, max_words=50,margin=5,mode="RGBA").generate(text)
    #FF0000
    wordcloud = WordCloud(stopwords=stopwords, background_color='#fcfcfa', max_words=50,margin=5,).generate(text)
    rcParams['figure.figsize'] = 20,20
    plt.imshow(wordcloud)
    plt.axis("off")
    desktop_path = os.path.join(os.path.expanduser("~"), 'C:/Users/prabh/OneDrive/Desktop/SIH/SIH-Ground1/SIH-Ground/public/Resources/')
    file_name = "my_word_cloud_excel_file.png"
    file_path = os.path.join(desktop_path, file_name)    
    
    plt.savefig(file_path, dpi=100, transparent=True)
    return

def word_bar_graph(text):
    text=" ".join(review for review in text)
    filtered_words = [word for word in text.split() if word not in STOPWORDS]
    counted_words = collections.Counter(filtered_words)
    words = []
    counts = []
    for letter, count in counted_words.most_common(10):
        words.append(letter)
        counts.append(count)
    words_json=json.dumps(words)
    counts_json=json.dumps(counts)
    return words_json,counts_json

def word_bar_graph_comment_static():
    data_initial=pd.read_csv("Twitter_Data.csv")
    data=pd.DataFrame()
    data["text"]=data_initial['clean_text'].iloc[152969:153969]
    data.dropna(inplace=True)
    text=data["text"]
    text=" ".join(review for review in text)
    filtered_words = [word for word in text.split() if word not in STOPWORDS]
    counted_words = collections.Counter(filtered_words)
    words_comment = []
    counts_comment = []
    for letter, count in counted_words.most_common(10):
        words_comment.append(letter)
        counts_comment.append(count)
    words_json=json.dumps(words_comment)
    counts_json=json.dumps(counts_comment)
    return words_json,counts_json

def word_bar_graph_excel_file(file_name):
    data_initial=pd.read_csv(file_name)
    data_initial.dropna(inplace=True)
    data=pd.DataFrame()
    data["text"]= data_initial["Text"]
    text=data['text']
    text=" ".join(review for review in text)    
    filtered_words = [word for word in text.split() if word not in STOPWORDS]
    counted_words = collections.Counter(filtered_words)
    words = []
    counts = []
    for letter, count in counted_words.most_common(10):
        words.append(letter)
        counts.append(count)
    words_json=json.dumps(words)
    counts_json=json.dumps(counts)
    return words_json,counts_json

@app.route('/predict', methods=['POST'])
def predict0() :
    try:
        data = request.json
        y = data["inputData"]
        data_twitter_handle = pd.DataFrame()
        data_twitter_handle["text"]= [y]
        # data_twitter_handle = get_all_tweets_data(y)
        # result = predict_function(data)
        wordImage = word_cloud(data_twitter_handle["text"])
        word_bargraph, count_bargraph = word_bar_graph(data_twitter_handle["text"])
        bert, percentage = predict_function_bert(data_twitter_handle["text"])
        return jsonify({"bert":bert, "word_bargraph":word_bargraph, "count_bargraph":count_bargraph, "percentage":percentage})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict_twitter', methods=['POST'])
def predict():
    try:
        data = request.json
        y = data["inputData"]
        data_twitter_handle = pd.DataFrame()
        # data_twitter_handle["text"]= ["i am good in various sports activites", "Narendra Modi is greatest personality in the field of literature and vedic maths"]
        data_twitter_handle = get_all_tweets_data(y)
        # result = predict_function(data)
        wordImage = word_cloud(data_twitter_handle["text"])
        word_bargraph, count_bargraph = word_bar_graph(data_twitter_handle["text"])
        bert, percentage = predict_function_bert(data_twitter_handle["text"])
        return jsonify({"bert":bert, "word_bargraph":word_bargraph, "count_bargraph":count_bargraph, "percentage":percentage})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/comments_twitter', methods=['GET'])
def predict2() :
    try:
        # data = request.json
        # y = data["inputData"]
        # data_twitter_handle["text"]= ["i am good in various sports activites", "Narendra Modi is greatest personality in the field of literature and vedic maths"]
        # data_twitter_handle = get_all_tweets_data(y)
        # result = predict_function_bert_comment_static()
        # wordImage = word_cloud1(data_twitter_handle["text"])
        # word_bargraph, count_bargraph = word_bar_graph(data_twitter_handle["text"])
        bert1, percentage1 = predict_function_bert_comment_static()
        word_cloud_comment_static()
        words, counts = word_bar_graph_comment_static()
        # print(bert1, percentage1)
        return jsonify({"bert":bert1, "percentage":percentage1, "words" : words, "counts": counts})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/youtube', methods=['POST'])
def predict4 () :
    try:
        data = request.json
        y = data["inputData"]
        data_youtube_handle = pd.DataFrame()
        # data_twitter_handle["text"]= ["i am good in various sports activites", "Narendra Modi is greatest personality in the field of literature and vedic maths"]
        data_youtube_handle = get_yt_data(y)
        # result = predict_function(data)
        wordImage = word_cloud(data_youtube_handle["text"])
        word_bargraph, count_bargraph = word_bar_graph(data_youtube_handle["text"])
        bert, percentage = predict_function_bert(data_youtube_handle["text"])
        return jsonify({"bert":bert, "word_bargraph":word_bargraph, "count_bargraph":count_bargraph, "percentage":percentage})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/excel', methods=['GET'])
def predict5 () :
    try:
        
        wordImage = world_cloud_excel_file('stock.csv')
        word_bargraph, count_bargraph = word_bar_graph_excel_file('stock.csv')
        bert, percentage = predict_function_excel_file('stock.csv')
        return jsonify({"bert":bert, "word_bargraph":word_bargraph, "count_bargraph":count_bargraph, "percentage":percentage})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

async def get_reddit(y):
    corou = await reddit_comments(y)
    return corou

@app.route('/reddit', methods=['POST'])
def predict6 () :
    try:
        data = request.json
        print(data)
        y = data["inputData"]
        data_reddit_handle = pd.DataFrame()
        corou = get_reddit(y)
        corou
        # result = predict_function(data)
        wordImage = word_cloud(corou["text"])
        word_bargraph, count_bargraph = word_bar_graph(corou["text"])
        bert, percentage = predict_function_bert(corou["text"])
        return jsonify({"bert":bert, "word_bargraph":word_bargraph, "count_bargraph":count_bargraph, "percentage":percentage})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=5000)

# %%
