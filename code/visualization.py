import json 
import operator
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates

############# Visualization One #############

months_2020 = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."]

months_2021 = ["January 2021", "February 2021", "March 2021", "April 2021", "May 2021", "June 2021", "July 2021", "August 2021", "September 2021", "October 2021", "November 2021", "December 2021"]

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
    pass 


############# Visualization Two #############


def visualization_two():
    pass 


############# Main #############


def main():
    visualization_one() 

if __name__ == "__main__":
    main() 

