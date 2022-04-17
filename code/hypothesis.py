
import json
from preprocess import terms
import numpy as np
"""
Calculates tweet_virality. Datum represents tweet objects in tweets_clean.json
Make sure tweets are from tweets_clean.json files
"""
def tweet_virality(datum):
    assert("reply_count" in datum)
    assert("retweet_count" in datum)
    assert("like_count" in datum)
    assert("quote_count" in datum)
    return datum["reply_count"] + datum["retweet_count"] + datum["like_count"] + datum["quote_count"]

"""
Helper that loads json objects
"""
def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

"""
Helper that saves json objects
"""
def save_json(path, obj):
    with open(path, 'w') as f:
        return json.dump(obj, f)

"""
Hypothesis #3a
What COVID keywords do the tweets need to contain in order for the tweet to have a high virality number?
For each keyword, Calculate number of posts per each range that contained that specific keyword
"""
def keywords_with_high_virality():
    cnn_tweets_read_path = "../data_clean/cnn_tweets_clean.json"
    fox_tweets_read_path = "../data_clean/fox_tweets_clean.json"
    out_path = "../data_clean/keywords_viralities.json"
    all_tweets = load_json(cnn_tweets_read_path) + load_json(fox_tweets_read_path)
    keywords_with_viralities = {}
    for keyword in terms:
        viralities = []
        for tweet in all_tweets:
            keyword in tweet["keywords"] and viralities.append(tweet_virality(tweet))
        viralities = sorted(viralities)
        if len(viralities) == 0: continue
        keywords_with_viralities[keyword] = {
            "0 - 200": len(list(filter(lambda x: x >= 0 and x < 200, viralities))),
            "200 - 400":len(list(filter(lambda x: x >= 200 and x < 400, viralities))),
            "400 - 600":len(list(filter(lambda x: x >= 400 and x < 600, viralities))),
            "600 - 800":len(list(filter(lambda x: x >= 600 and x < 800, viralities))),
            "800+":len(list(filter(lambda x: x >= 800, viralities))),
        }
    return save_json(out_path, keywords_with_viralities)
      
"""
Hypothesis #3b
Are there certain months in which tweeting with a certain COVID keyword will lead to a high virality number? 
"""

def keywords_with_high_virality_per_month():
    cnn_replies_read_path = "../data_clean/cnn_replies_clean.json"
    fox_tweets_read_path = "../data_clean/fox_tweets_clean.json"
    out_path = "../data_clean/keywords_viralities_per_month.json"

    





def main():
    keywords_with_high_virality()

if __name__ == "__main__":
    main() 
