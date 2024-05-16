import json
import ast
from pre_class import BuildFreqs,ProcessTweets,ExtractFeatuers

from sklearn.pipeline import Pipeline


pre_processing_pipline = Pipeline([

    ('clean_tweets',ProcessTweets()),
    ('clean_freqs', BuildFreqs())

])


pre_processing_pipline_new_data = Pipeline([

    ('clean_tweets',ProcessTweets()),
    ('feature_extract' , ExtractFeatuers()),
    
])


