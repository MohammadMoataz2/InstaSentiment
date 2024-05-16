
from sklearn.base import TransformerMixin, BaseEstimator
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
import seaborn as sns
import matplotlib.patheffects as path_effects
import emoji
class ProcessTweets(BaseEstimator,TransformerMixin):

    def __init__(self):
        self.string = string
        self.processed_tweets = None
        self.ready_tweets = None


    def fit(self,X,y = None):
        self.proccesed_tweets = X


    
    def transform(self, X):

        under_tweets = X
        
        if type(under_tweets) == str:

            under_tweets = [under_tweets]




        """Process tweet function.
        Input:
            tweet: a string containing a tweet
        Output:
            tweets_clean: a list of words containing the processed tweet

        """
        stemmer = PorterStemmer()
        stopwords_english = stopwords.words('english')





        sub_tweets = []
        for tweet in under_tweets:

            tweet = emoji.demojize(tweet)
            
            
            # remove stock market tickers like $GE
            tweet = re.sub(r'\$\w*', '', tweet)
            # remove old style retweet text "RT"
            tweet = re.sub(r'^RT[\s]+', '', tweet)
            # remove hyperlinks
            tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
            # remove hashtags
            # only removing the hash # sign from the word
            tweet = re.sub(r'#', '', tweet)

            

            sub_tweets.append(tweet)


            

        # tokenize tweets
        tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,
                                reduce_len=True)
        

        tokenize_tweets = []
        for tweet in sub_tweets:
            tokenize_tweets.append(tokenizer.tokenize(tweet)) 


        clean_tweets = []

        for single_tweet in tokenize_tweets:
            tweet_clean = []
            for word in single_tweet:


                if (word not in stopwords_english and  # remove stopwords
                        word not in string.punctuation):  # remove punctuation
                    
                    # tweets_clean.append(word)
                    stem_word = stemmer.stem(word)  # stemming word
                    tweet_clean.append(stem_word)

            clean_tweets.append(" ".join(tweet_clean))


        if self.ready_tweets == None:
            self.ready_tweets = clean_tweets


        return  clean_tweets
    


    
    def fit_transform(self,X,y=None):
        self.fit(X,y)

        return self.transform(X)










class BuildFreqs(BaseEstimator,TransformerMixin):
    def __init__(self):
        self.tweets = None
        self.labels = None
        self.freqs = None
        

    def fit(self,X,y = None):

        self.tweets = X
        self.labels = y

        

    def transform(self,X):


        tweets = X
        ys = self.labels
        

        if type(tweets) == str:

            under_tweets = [under_tweets]

        """Build frequencies.
        Input:
            tweets: a list of tweets
            ys: an m x 1 array with the sentiment label of each tweet
                (either 0 or 1)
        Output:
            freqs: a dictionary mapping each (word, sentiment) pair to its
            frequency
        """
        # Convert np array to list since zip needs an iterable.
        # The squeeze is necessary or the list ends up with one element.
        # Also note that this is just a NOP if ys is already a list.
        yslist = np.squeeze(ys).tolist()

        # Start with an empty dictionary and populate it by looping over all tweets
        # and over all processed words in each tweet.
        freqs = {}
        for y, tweet in zip(yslist, tweets):
            for word in tweet.split(" "):
                if word == "::":
                    continue
                pair = (word, y)
                if pair in freqs:
                    freqs[pair] += 1
                else:
                    freqs[pair] = 1


        if self.freqs == None:
            self.freqs = freqs


        return freqs
    


    def fit_transform(self,X,y = None):
        self.fit(X,y)

        return self.transform(X)
        



class ExtractFeatuers(BaseEstimator,TransformerMixin):
    def __init__(self):
        self.tweets = None
        self.freqs = None
        self.extracted_featuers = None

    def fit(self,X,y = None):

        self.tweets = X
        self.freqs = y

    def transform(self,X):
        cleaned_tweets = X

        freqs = self.freqs

        if type(cleaned_tweets) == str:
            cleaned_tweets = [cleaned_tweets]


        '''
        Input: 
            tweet: a list of words for one tweet
            freqs: a dictionary corresponding to the frequencies of each tuple (word, label)
        Output: 
            x: a feature vector of dimension (1,3)
        '''
        # process_tweet tokenizes, stems, and removes stopwords
        list_of_extract_featuers = []


        for single_tweet in cleaned_tweets:
            x = np.zeros((1, 3)) 
            
            #bias term is set to 1
            x[0,0] = 1

            for word in single_tweet.split():

                
                        
                # increment the word count for the positive label 1
                x[0,1] += freqs.get((word, 1.0),0)
                
                # increment the word count for the negative label 0
                x[0,2] += freqs.get((word, 0.0),0)

                

            list_of_extract_featuers.append(x.flatten())

        if self.extracted_featuers == None:
            self.extracted_featuers = list_of_extract_featuers
            
        return list_of_extract_featuers
        

    def fit_transform(self,X,y = None):
        self.fit(X,y)

        return self.transform(X)
        