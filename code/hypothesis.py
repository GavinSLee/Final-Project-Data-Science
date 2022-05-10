
import json
from preprocess import terms
import numpy as np
import pandas as pd
from scipy.stats import ttest_1samp, ttest_ind, ttest_rel, chi2_contingency


########## Util Functions ###########

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
    tstats, pvalue = ttest_ind(values_a, values_b, nan_policy = 'omit')

    # and then we'll return tstats and pvalue
    return tstats, pvalue

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


########## Hypothesis One ###########


def hypothesis_one():
    """
    Hypothesis 1: Does CNN focus more on certain keywords more than Fox? 

    To do this, we state the null hypothesis: there is no difference in the population proportion between Fox News and CNN for tweets that contain some certain keyword. 

    Article reference: https://www.dataquest.io/blog/tutorial-text-analysis-python-test-hypothesis/

    Returns the following: {keyword : (conf lower, conf upper)}, {keyword: (cnn prop, fox prop)}

    """
    cnn_tweets_list = load_json("../data_clean/cnn_tweets_clean.json")
    fox_tweets_list = load_json("../data_clean/fox_tweets_clean.json")

    hyp_one_dict = {} 

    for term in terms:
        metrics = get_ci_range(term, cnn_tweets_list, fox_tweets_list)     
        conf_bound = metrics[0] 
        conf_lower_bound = conf_bound[0] 
        conf_upper_bound = conf_bound[1] 
        props = metrics[1] 
        cnn_prop = props[0] 
        fox_prop = props[1] 

        hyp_one_dict[term] = {"conf lower bound" : conf_lower_bound, "conf upper bound": conf_upper_bound, "cnn prop" : cnn_prop, "fox_prop" : fox_prop}

    save_json("../data_hypotheses/hypothesis_1.json", hyp_one_dict)

def get_ci_range(word, cnn_tweets_list, fox_tweets_list):

    cnn_tweets_containing_word = [] 
    for tweet in cnn_tweets_list:
        tweet_keywords = tweet["keywords"]
        for keyword in tweet_keywords:
            if word == keyword:
                cnn_tweets_containing_word.append(tweet) 
                break 
    
    fox_tweets_containing_word = [] 
    for tweet in fox_tweets_list:
        tweet_keywords = tweet["keywords"]
        for keyword in tweet_keywords:
            if word == keyword:
                fox_tweets_containing_word.append(tweet) 
                break 
    
    num_cnn_tweets_contain_word = len(cnn_tweets_containing_word) 
    num_cnn_tweets = len(cnn_tweets_list)

    cnn_word_prop = num_cnn_tweets_contain_word / num_cnn_tweets 

    num_fox_tweets_contain_word = len(fox_tweets_containing_word) 
    num_fox_tweets = len(fox_tweets_list) 

    fox_word_prop = num_fox_tweets_contain_word / num_fox_tweets 

    return [calc_ci_range(cnn_word_prop, num_cnn_tweets, fox_word_prop, num_cnn_tweets), (cnn_word_prop, fox_word_prop)]

def standard_err(p1, n1, p2, n2):
    return np.sqrt((p1* (1-p1) / n1) + (p2 * (1-p2) / n2))

def ci_range(diff, std_err, cv = 1.96):
    return (diff - cv * std_err, diff + cv * std_err)

def calc_ci_range(p1, n1, p2, n2):
    std_err = standard_err(p1, n1, p2, n2)
    diff = p1-p2
    return ci_range(diff, std_err)


########## Hypothesis Two ###########


def hypothesis_two():

    cnn_tweets = load_json("../data_clean/cnn_tweets_clean.json")
    cnn_replies = load_json("../data_clean/cnn_replies_clean.json") 

    fox_tweets = load_json("../data_clean/fox_tweets_clean.json") 
    fox_replies = load_json("../data_clean/fox_replies_clean.json") 

    hyp_two_dict = {} 

    for keyword in terms:
        tstats, p_value, cnn_avg_sentiment, fox_avg_sentiment = calculate_ttest_metrics(keyword, cnn_tweets, cnn_replies, fox_tweets, fox_replies) 
        metrics_dict = {"tstats": 0, "p-value": 0, "cnn_avg_sentiment": 0, "fox_avg_sentiment": 0}
        metrics_dict["tstats"] = tstats 
        metrics_dict["p-value"] = p_value 
        metrics_dict["cnn_avg_sentiment"] = cnn_avg_sentiment
        metrics_dict["fox_avg_sentiment"] = fox_avg_sentiment 
        hyp_two_dict[keyword] = metrics_dict

    save_json("../data_hypotheses/hypothesis_2.json", hyp_two_dict)
    

def calculate_ttest_metrics(keyword, cnn_tweets, cnn_replies, fox_tweets, fox_replies):
    """
    We want to determine the average sentiment of reply tweets for certain covid keywords differs between Fox & CNN. 
    """

    cnn_replies_sublist = get_sublist_replies(keyword, cnn_tweets, cnn_replies) 
    fox_replies_sublist = get_sublist_replies(keyword, fox_tweets, fox_replies) 

    cnn_sentiment_scores = get_sentiment_scores_list(cnn_replies_sublist) 
    fox_sentiment_scores = get_sentiment_scores_list(fox_replies_sublist) 
    
    cnn_avg_sentiment = 0 
    fox_avg_sentiment = 0 

    if len(cnn_sentiment_scores) > 0:
        cnn_avg_sentiment = sum(cnn_sentiment_scores) / len(cnn_sentiment_scores) 
    if len(fox_sentiment_scores) > 0:
        fox_avg_sentiment = sum(fox_sentiment_scores) / len(fox_sentiment_scores) 
    
    tstats, p_value = two_sample_ttest(cnn_sentiment_scores, fox_sentiment_scores) 
    return tstats, p_value, cnn_avg_sentiment, fox_avg_sentiment

def get_sublist_replies(keyword, tweets, replies):
    # First, iterate through tweets and see if it contains one of the covid keywords. If it does, append the tweet id to a list of tweet_ids.

    tweet_ids_set = set() 

    for tweet in tweets:
        keywords = tweet["keywords"]
        tweet_id = tweet["id"]
        if keyword in keywords:
            tweet_ids_set.add(tweet_id)
    
    reply_subset = [] 
    # Then, get subset of replies in which the reply has a conversation ID that matches one of the keys in the tweet_ids_set
    for reply in replies: 
        conversation_id = reply["conversation_id"]
        if conversation_id in tweet_ids_set:
            reply_subset.append(reply)

    return reply_subset  
        

def get_sentiment_scores_list(replies_subset):
    sentiment_scores = [] 
    for reply in replies_subset:
        sentiment_score = reply["adjusted_sentiment_score"]
        sentiment_scores.append(sentiment_score) 
    
    return sentiment_scores 


########## Hypothesis Three (OLD) ###########

"""
Hypothesis 3: Does a tweet containing a certain COVID keyword lead to virality? 

Null Hypothesis: No relationship exists between the two categorical variables. 
Reject if the p-value is less than .05. 

"""
def hypothesis_three(): 
    MIN_VIRAL = 800 # viral posts must be 800 and over
    cnn_tweets_read_path = "../data_clean/cnn_tweets_clean.json"
    fox_tweets_read_path = "../data_clean/fox_tweets_clean.json"
    out_path = "../data_hypotheses/hypothesis_3.json"
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
            if tweet_virality(tweet) >= MIN_VIRAL:
                is_viral.append(1)
            else:
                is_viral.append(0)
        if not np.any(has_keyword_list): continue
        df = pd.DataFrame(data={"keyword" : has_keyword_list, "viral": is_viral})
        tstats, pval = chisquared_independence_test(df, "keyword", "viral")
        result[keyword] = {"chi2": tstats, "p-value": pval}
    save_json(out_path, result)

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
Hypothesis #3a
What COVID keywords do the tweets need to contain in order for the tweet to have a high virality number?
For each keyword, Calculate number of posts per each range that contained that specific keyword
"""
def keywords_with_virality():
    cnn_tweets_read_path = "../data_clean/cnn_tweets_clean.json"
    fox_tweets_read_path = "../data_clean/fox_tweets_clean.json"
    out_path = "../data_hypotheses/keywords_viralities.json"
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
    out_path = "../data_hypotheses/keywords_viralities_per_month.json"
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

def calculate_avg_virality_prop():
    viralities_path = "../data_hypotheses/keywords_viralities.json"
    viralities_dict = load_json(viralities_path) 

    for keyword in viralities_dict:
        keyword_dict = viralities_dict[keyword] 
        count = 0 
        for viral_range in keyword_dict:
            count += keyword_dict[viral_range] 
        
        viral_prop = keyword_dict["800+"] / count 
        keyword_dict["viral_prop"] = viral_prop 
    
    save_json(viralities_path, viralities_dict)


def main():

    hyp_one_result = hypothesis_one() 
    # hyp_two_result = hypothesis_two() 
    # keywords_with_virality_per_month() 
    # calculate_avg_virality_prop() 
    # keywords_with_virality() 


if __name__ == "__main__":
    main() 
