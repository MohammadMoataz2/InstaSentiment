from piplines import pre_processing_pipline,pre_processing_pipline_new_data
import nltk                                # Python library for NLP
from nltk.corpus import twitter_samples    # sample Twitter dataset from NLTK
import matplotlib.pyplot as plt      
import random                              # pseudo-random number generator      # library for visualization
import re
import string
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer
import pathlib


def Predict_tweet(tweets):

    if type(tweets) == str:
        tweets = [tweets]

    if type(tweets) == pd.core.frame.DataFrame:
        tweets = tweets.values

    # all_positive_tweets = twitter_samples.strings('positive_tweets.json')
    # all_negative_tweets = twitter_samples.strings('negative_tweets.json')




    # print(f"The Length of The Positive Tweets {len(all_positive_tweets)}")
    # print(f"The Length of The Negative Tweets {len(all_negative_tweets)}")

    # dict_tweets = {

    #     "Positive Tweets":all_positive_tweets,
    #     "Negative tweets":all_negative_tweets,
    #     "all_tweets" :all_positive_tweets+all_negative_tweets
    # }

    # labels = np.append(np.ones((len(all_positive_tweets))), np.zeros((len(all_negative_tweets))))

    # labels_names = ["Positive" , "Negative"]


    # #print(pre_processing_pipline.fit_transform(dict_tweets["all_tweets"],labels))

    import json
    import ast
    import os
    import pickle
    # Get the current working directory
    folder_path = str(pathlib.Path().resolve()) + "\\"


    freqs_json_file = fr"{folder_path}freqs.json"

    with open(freqs_json_file, "r") as json_file:
        loaded_data = json.load(json_file)

    cleaned_freqs = {ast.literal_eval(key): value for key, value in loaded_data.items()}

    print(tweets)
  

    cleaned_featuers = pre_processing_pipline_new_data.fit_transform(tweets,cleaned_freqs)





    model_pkl_file = fr"{folder_path}RF_model.pkl"

    with open(model_pkl_file, 'rb') as file:  
        model = pickle.load(file)


    return model.predict(cleaned_featuers)