import json 
import operator
import pandas as pd 
import numpy as np 
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
from matplotlib.dates import DateFormatter


############# Visualization One #############

months_2020 = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."]
full_months_2020 = ["January 2020", "February 2020", "March 2020", "April 2020", "May 2020", "June 2020", "July 2020", "August 2020", "September 2020", "October 2020", "November 2020", "December 2020"]
months_2021 = ["January 2021", "February 2021", "March 2021", "April 2021", "May 2021", "June 2021", "July 2021", "August 2021", "September 2021", "October 2021", "November 2021", "December 2021"]
full_months = full_months_2020 + months_2021
months = months_2020 + months_2021

def sort_keyword_freq_dict(keyword_freq_dict, news_outlet): 
    """
    Appropriately sorts the keyword dict for easier visualization. 
    """

    months_dict = keyword_freq_dict[news_outlet]


    for month in months_dict: 
        keywords_dict = months_dict[month]
        sorted_keywords_dict = dict(sorted(keywords_dict.items(), key = operator.itemgetter(1), reverse = True))
        months_dict[month] = sorted_keywords_dict 


    return keyword_freq_dict

def get_keyword_freq_json(news_tweets_list): 
    """
    Example dictionary - {
        "CNN" : {
            "January 2020" : {
                "Trump" : 5, 
                "Vaccines" 7, 
                "Masks 9"
            }, 
            "February 2020" : {
                "Lockdowns" 9, 
                "wuhan": 19
            }
        }    
    }
    """
    news_outlet = news_tweets_list[0]["news_outlet"]

    keyword_freq_dict = {news_outlet : {}}

    for month in months: 
        keyword_freq_dict[news_outlet][month] = {} 

    for tweet in news_tweets_list: 
        
        month = tweet["month"]
        keywords = tweet["keywords"]
        
        month_dict = keyword_freq_dict[news_outlet]

        keywords_dict = month_dict[month]

        if "num_news_tweets_this_month" not in keywords_dict:
            keywords_dict["num_news_tweets_this_month"] = 1
        else:
            keywords_dict["num_news_tweets_this_month"] += 1

        if len(keywords) > 0:
            if "num_news_tweets_contain_keyword" not in keywords_dict:
                keywords_dict["num_news_tweets_contain_keyword"] = 1
            else:
                keywords_dict["num_news_tweets_contain_keyword"] += 1
        
        for keyword in keywords:
            if keyword not in keywords_dict:
                keywords_dict[keyword] = 1
            else:
                keywords_dict[keyword] += 1


    keyword_freq_dict = sort_keyword_freq_dict(keyword_freq_dict, news_outlet) 

    return [keyword_freq_dict] 


def load_data(file_path):
    """
    Loads the data and returns the list of tweets (dictionaries). 
    """
    with open(file_path, 'r') as f:
        data = json.load(f) 
    return data 

def write_data(file_path, data):
    """
    Writes the data to a file. 
    """

    with open(file_path, 'w') as f:
        json.dump(data, f) 

def build_keyword_json_files():
    cnn_tweets_clean_path = "../data_clean/cnn_tweets_clean.json"
    cnn_keyword_freq_json_path = "../data_clean/cnn_keyword_freq.json"
    fox_tweets_clean_path = "../data_clean/fox_tweets_clean.json"
    fox_keyword_freq_json_path = "../data_clean/fox_keyword_freq.json"
    
    cnn_tweets_list = load_data(cnn_tweets_clean_path)
    fox_tweets_list = load_data(fox_tweets_clean_path) 
    
    cnn_keyword_freq_json = get_keyword_freq_json(cnn_tweets_list)
    fox_keyword_freq_json = get_keyword_freq_json(fox_tweets_list) 

    write_data(cnn_keyword_freq_json_path, cnn_keyword_freq_json)
    write_data(fox_keyword_freq_json_path, fox_keyword_freq_json)

def visualization_one():
    # Plot 1
    cnn_data = load_data("data_clean/cnn_keyword_freq.json")
    fox_data = load_data("data_clean/fox_keyword_freq.json")
    
    percent_tweets_with_keywords = []
    percent_tweets_with_keywords_fox = []
    
    for m in full_months:
        curr_month_data = cnn_data[0]['CNN'][m]
        curr_month_data_fox = fox_data[0]['Fox News'][m]
        percent_tweets_with_keywords.append(curr_month_data["num_news_tweets_contain_keyword"]/curr_month_data["num_news_tweets_this_month"])
        if "num_news_tweets_contain_keyword" in curr_month_data_fox and "num_news_tweets_this_month" in curr_month_data_fox:
            percent_tweets_with_keywords_fox.append(curr_month_data_fox["num_news_tweets_contain_keyword"]/curr_month_data_fox["num_news_tweets_this_month"])
        else:
            percent_tweets_with_keywords_fox.append(0)
    # CNN
    fig, ax = plt.subplots()
    ax.plot(full_months,percent_tweets_with_keywords)

    fig.autofmt_xdate()
    ax.set_xlabel('months')
    ax.set_ylabel('ratio')
    ax.set_title('Ratio of number of news tweets containing keyword to number of news tweets this month in CNN news')
    plt.show()
    
    # FOX
    fig, ax = plt.subplots()
    ax.plot(full_months,percent_tweets_with_keywords_fox)

    fig.autofmt_xdate()
    ax.set_xlabel('months')
    ax.set_ylabel('ratio')
    ax.set_title('Ratio of number of news tweets containing keyword to number of news tweets this month in FOX news')
    plt.show()
    
    # Plot 2
    key_words = ["pandemic", "trump", "dem", "vaccine", "variant", "biden"]

    curr_key_vals = []
    curr_key_vals_fox = []
    for key in key_words:
        for m in full_months:
            curr_month_data = cnn_data[0]['CNN'][m]
            
            if key in curr_month_data:
                curr_key_vals.append(curr_month_data[key])
            else:
                curr_key_vals.append(0)

        plt.plot(full_months,curr_key_vals, label = key)
        curr_key_vals = []
    plt.gcf().autofmt_xdate()
    plt.xlabel('months')
    plt.ylabel('count')
    plt.title('Monthly frequency of each keyword on CNN, 2020-2021')
    plt.legend()
    plt.show()
    
    for key in key_words:
        for m in full_months:
            curr_month_data_fox = fox_data[0]['Fox News'][m]
            if key in curr_month_data_fox:
                curr_key_vals_fox.append(curr_month_data_fox[key])
            else:
                curr_key_vals_fox.append(0)
        plt.plot(full_months,curr_key_vals_fox, label = key)
        curr_key_vals_fox = []
    plt.gcf().autofmt_xdate()
    plt.xlabel('months')
    plt.ylabel('count')
    plt.title('Monthly frequency of each keyword on Fox news, 2020-2021')
    plt.legend()
    plt.show()
    
        
    
############# Visualization One #############


def visualization_two():
    pass 


############# Visualization for Hypothesis One #############

def visualization_one_hyp():
    keywords = ["trump", "biden", "abbott", "cuomo", "fauci", "democrat", "republican", "vaccine"]
    cnn_proportions = [0.056, 0.051, 0.004, 0.006, 0.024, 0.013, 0.017, 0.157]
    fox_proportions = [0.059, 0.120, 0.007, 0.037, 0.036, 0.016, 0.015, 0.215]

    prop_dict = {"keywords": keywords, "cnn proportions" : cnn_proportions, "fox proportions": fox_proportions}

    # df = pd.DataFrame(prop_dict) 
    

    x_axis = np.arange(len(keywords))


    plt.figure(figsize = (10, 16))
    plt.bar(x_axis - 0.2, cnn_proportions, 0.4, label = 'CNN Proportion', color = 'red')
    plt.bar(x_axis + 0.2, fox_proportions, 0.4, label = 'Fox Proportion', color = 'blue')
    plt.xticks(x_axis, keywords)
    plt.xlabel("keywords")
    plt.ylabel("proportion")
    plt.title("Proportion of News Tweets That Contain Keyword for CNN vs Fox")
    plt.legend() 

    plt.show() 


############# Visualization for Hypothesis Two #############
def visualization_two_hyp():

    types = ['trump', 'biden', 'fauci', 'democrat', 'republican', 'vaccine', 'mask', 'lockdown', 'quarantine', 'cuomo', 'abbott']
    x_coords = [-0.38, -0.24, -0.29, -0.33, -0.38, -0.242, -0.313, -0.252, -0.259, -0.340, -0.308]
    y_coords = [-0.34, -0.31, -0.33, -0.34, -0.406, -0.263, -0.295, -0.403, -0.285, -0.340, -0.289]

    plt.figure(figsize = (10, 10))
    for i,type in enumerate(types):
        x = x_coords[i]
        y = y_coords[i]
        plt.scatter(x, y, marker='o', color='blue')
        plt.text(x+0.3, y+0.3, type, fontsize=9)
        plt.annotate(type, (x, y), xytext = (x - .003, y + .002)) 

    plt.xlabel("CNN Average Sentiment Score")
    plt.ylabel("Fox Average Sentiment Score")
    plt.title("Scatter Plot of Average Sentiment Score for Various Keywords for Fox and CNN")
    plt.show()

############# Visualization for Hypothesis Three #############

def visualization_three_hyp():
    pass 





############# Main #############


def main():
    visualization_one_hyp() 
    # visualization_two_hyp() 

if __name__ == "__main__":
    main() 

