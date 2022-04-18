
import json
from preprocess import terms
import numpy as np
import pandas as pd
from scipy.stats import ttest_1samp, ttest_ind, ttest_rel, chi2_contingency


############## STATS TESTS ##########################
def chisquared_independence_test(df, column_a_name, column_b_name):
    ## Stencil: Error check input - do not modify this part
    # assert all_variable_names_in_df([column_a_name, column_b_name], df)

    # TODO: Create a cross table between the two columns a and b
    # Hint: If you are unsure how to do this, refer to the stats lab!
    cross_table = pd.crosstab(df[column_a_name], df[column_b_name])

    # TODO: Use scipy's chi2_contingency
    # (https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html)
    # to get the test statistic and the p-value
    tstats, pvalue, dof, expected = chi2_contingency(cross_table)

    # TODO: You can print out the test statistics and pvalue to determine your answer
    # to the questions
    print("tstats: ", tstats)
    print("p value: ", pvalue)

    # and then we'll return tstats and pvalue
    return tstats, pvalue

def two_sample_ttest(values_a, values_b):
    ## Stencil: Error check input - do not modify this part
    
    # TODO: Use scipy's ttest_ind
    # (https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html)
    # to get the t-statistic and the p-value
    # Note: Be sure to make the function call in a way such that the code will disregard
    # null (nan) values. Additionally, you can assume equal variance.
    tstats, pvalue = ttest_ind(values_a, values_b)

    # TODO: You can print out the tstats, pvalue, and other necessary
    # calculations to determine your answer to the questions
    print("tstats: ", tstats)
    print("p value: ", pvalue)

    # and then we'll return tstats and pvalue
    return tstats, pvalue

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

##################### HYPOTHESIS #################################

"""
Hypothesis 1: Frequency of each keyword used between Fox and CNN
"""        
def hypothesis1():
    cnn_freq_read_path = "../data_clean/cnn_keyword_freq.json"
    fox_freq_read_path = "../data_clean/fox_keyword_freq.json"
    out_path = "../data_clean/hypothesis1.json"
    result = {}
    cnn_freq = load_json(cnn_freq_read_path)[0]["CNN"]
    fox_freq = load_json(fox_freq_read_path)[0]["Fox News"]
    for keyword in terms:
        is_fox = []
        keyword_freq = []
        for month in cnn_freq:
            cnn_freq_data = cnn_freq[month]
            fox_freq_data = fox_freq[month]
            cnn_keyword_freq = 0
            fox_keyword_freq = 0
            if keyword in cnn_freq_data:
                cnn_keyword_freq = cnn_freq_data[keyword]
            if keyword in fox_freq_data:
                fox_keyword_freq = fox_freq_data[keyword]
            is_fox.append(0)
            keyword_freq.append(cnn_keyword_freq)
            is_fox.append(1)
            keyword_freq.append(fox_keyword_freq)
        # df = pd.DataFrame(data={"fox" : is_fox, "frequency": keyword_freq})
        tstats, pval = two_sample_ttest(is_fox, keyword_freq)
        result[keyword] = {"tstats" : tstats, "p-value": pval}
    save_json(out_path, result)
    


    
"""
Hypothesis 3: Relationship between keyword vs virality of the content
"""
def hypothesis3(): 
    MIN_VIRAL = 800 #viral posts must be 800 and over
    cnn_tweets_read_path = "../data_clean/cnn_tweets_clean.json"
    fox_tweets_read_path = "../data_clean/fox_tweets_clean.json"
    out_path = "../data_clean/hypothesis3.json"
    all_tweets = load_json(cnn_tweets_read_path) + load_json(fox_tweets_read_path)
    result = {}
    for keyword in terms:
        has_keyword_list = []
        is_viral = []
        for tweet in all_tweets:
            if keyword in tweet["keywords"]:
                has_keyword_list.append(1)
            else:
                has_keyword_list.append(0)
            if tweet_virality(tweet) >= 800:
                is_viral.append(1)
            else:
                is_viral.append(0)
        if not np.any(has_keyword_list): continue
        df = pd.DataFrame(data={"keyword" : has_keyword_list, "viral": is_viral})
        tstats, pval = chisquared_independence_test(df, "keyword", "viral")
        result[keyword] = {"tstats": tstats, "p-value": pval}
    save_json(out_path, result)






############################## OLD WORK (might be useful for visualization later #####################################
"""
Hypothesis #3a
What COVID keywords do the tweets need to contain in order for the tweet to have a high virality number?
For each keyword, Calculate number of posts per each range that contained that specific keyword
"""
def keywords_with_virality():
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

def keywords_with_virality_per_month():
    cnn_tweets_read_path = "../data_clean/cnn_tweets_clean.json"
    fox_tweets_read_path = "../data_clean/fox_tweets_clean.json"
    out_path = "../data_clean/keywords_viralities_per_month.json"
    months_2020 = ["January 2020", "February 2020", "March 2020", "April 2020", "May 2020", "June 2020", "July 2020", "August 2020", "September 2020", "October 2020", "November 2020", "December 2020"]
    months_2021 = ["January 2021", "February 2021", "March 2021", "April 2021", "May 2021", "June 2021", "July 2021", "August 2021", "September 2021", "October 2021", "November 2021", "December 2021"]
    months = months_2020 + months_2021
    all_tweets = load_json(cnn_tweets_read_path) + load_json(fox_tweets_read_path)
    result = {}
    for keyword in terms:
        data = {}
        for m in months:
            data[m] = {"total": 0, "count": 0}
        for tweet in all_tweets:
            if keyword not in tweet["keywords"]: continue
            month = tweet["month"]
            virality = tweet_virality(tweet)
            data[month]["total"] += virality
            data[month]["count"] += 1
        total_count = 0 #this is for tracking if keyword has been used 
        for month, datum in data.items():
            if datum["count"] == 0:
                data[month] = 0
            else:
                total_count += datum["count"]
                data[month] = datum["total"] / datum["count"]
        if total_count == 0: continue
        result[keyword] = data
    save_json(out_path, result)


        
def get_subset_replies(covid_keywords_set, tweets, replies):
    # First, iterate through tweets and see if it contains one of the covid keywords. If it does, append the tweet id to a list of tweet_ids.

    tweet_ids_set = set() 

    for tweet in tweets:
        keywords = tweet["keywords"]
        tweet_id = tweet["id"]
        for keyword in keywords:
            if keyword in covid_keywords_set: 
                tweet_ids_set.add(tweet_id) 
                break 
    
    reply_subset = [] 
    # Then, get subset of replies in which the reply has a conversation ID that matches one of the keys in the tweet_ids_set
    for reply in replies: 
        conversation_id = reply["conversation_id"]
        if conversation_id in tweet_ids_set:
            reply_subset.append(reply)

    return reply_subset  
        

def hypothesis2():
    """
    We want to determine the average sentiment of reply tweets for certain covid keywords differs between Fox & CNN. 
    """
    cnn_tweets_path = "../data_clean/cnn_tweets_clean.json"
    cnn_replies_path = "../data_clean/cnn_replies_clean.json"

    fox_tweets_path = "../data_clean/fox_tweets_clean.json"
    fox_replies_path = "../data_clean/fox_replies_clean.json"

    cnn_tweets = load_json(cnn_tweets_path)
    cnn_replies = load_json(cnn_replies_path) 

    fox_tweets = load_json(fox_tweets_path) 
    fox_replies = load_json(fox_replies_path) 

    
    # First, get replies that correspond to the list of covid keywords that we want
    keywords_subset = {"fauci", "trump", "biden"}
    replies_subset = get_subset_replies(keywords_subset, cnn_tweets, cnn_replies) 

    print(replies_subset) 




def main():
    hypothesis1()


if __name__ == "__main__":
    main() 
