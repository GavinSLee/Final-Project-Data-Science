
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


            
        


    


def main():
    hypothesis3()


if __name__ == "__main__":
    main() 
