from asyncio.proactor_events import _ProactorWritePipeTransport
from json.tool import main
import json 
import subprocess
import os 

"""
This file is responsible for scraping covid related tweets from CNN and Fox News from January 2020 - December 2021. We use the library snscrape to gather the tweets, and this library simplifies our work by no longer needing to use a web browser based scraper (like selenium) to gather the tweets. 

The data is first written as jsonl (json lines) files in the directory: data_dirty. Then, we parse through the files, removing some unnecessary attributes. We write the clean data as json files to data_clean.  

To run this file, use the command: python code/news_tweets.py in your shell. 
"""

def scrape_tweets(news_outlet, keywords, begin_dates, end_dates):
    """
    This is the main method that scrapes tweets using the snscrape library. The snscrape library mainly uses a CLI; however, we can make use of python's OS package to scrape more programmatically. We iterate by month. 

    :param news_outlet: string (news outlet we want to scrape for)
    :param keywords: list (keywords that we want to base our search query off of)
    :param begin_dates: list (list of the first of each month that we want to search off of)
    :param end_dates: list (list of the end of each month that we want to search off of)
    :param months: list (what month we're searching for)

    :returns: None (writes the parsed result to a file in the ./data_clean directory)
    """

    # We gather tweets per month. 
    for i in range(len(begin_dates)):
        begin_date = begin_dates[i] 
        end_date = end_dates[i] 

        # Snscrape uses a CLI command to scrape tweets. The parameters --jsonl writes the scraped data to a json file, and --progress prints scraped data progress. 
        base_command = "snscrape --jsonl --progress --max-results 150 --since " + begin_date + " twitter-search "
        if news_outlet == "CNN":
            path = "./data_dirty/cnn_tweets_2021_dirty.jsonl"  
        else:
            path = "./data_dirty/fox_tweets_2021_dirty.jsonl"

        # Gather covid related tweets per our defined keywords, for each news outlet. 
        for keyword in keywords:
            query_param = keyword + " "
            from_param = "from:" + news_outlet + " "
            until_param = "until:" + end_date 
            search_command = "\"" + query_param + from_param + until_param + "\""

            # Will write the output to some dirty file 
            output = " >> " + path 
            final_command = base_command + search_command + output 
            print(final_command)
            os.system(final_command) 
    
def parse_jsonl_file(dirty_path, clean_path, months_mapping):

    with open(dirty_path, 'r') as dirty_json_file:
        json_list = list(dirty_json_file) 
    
    keys_to_remove = ["_type", "user", "source", "sourceUrl", "sourceLabel", "tcooutlinks", "media", "retweetedTweet", "quotedTweet", "inReplyToTweetId", "inReplyToUser", "mentionedUsers", "coordinates", "place", "cashtags", "renderedContent"]
    tweets_list = []
    for json_str in json_list:
        json_line = json.loads(json_str) 
        for key in keys_to_remove:
            json_line.pop(key) 
        date = json_line["date"]
        date = date[0:7] 
        json_line["month"] = months_mapping[date]
        tweets_list.append(json_line) 
    
    with open(clean_path, 'w') as clean_json_file:
        json.dump(tweets_list, clean_json_file) 
        
def get_covid_keywords():
    """
    Defines keywords that we pass to the search query.
    returns: final keywords (list) 
    """
    
    # Keywords are separated by category, and then the lists are concatenated at the end to make the final keywords list. 
    covid_keywords = ["coronavirus", "corona virus", "corona", "covid", "covid19", "covid-19", "covid 19", "sarscov2", "sars cov 2", "wuhan virus"]
    # variants_keywords = ["delta variant", "omicron", "omicron variant", "variant", "variants"]
    # pandemic_keywords = ["pandemic", "quarantine", "self-quarantine", "self quarantine", "self-isolation", "self isolation", "lockdown", "social distancing", "social distance", "flattening the curve", "flatten the curve", "herd immunity", "symptomatic", "asymptomatic"] 
    # vaccine_keywords = ["moderna", "pfizer", "johnson & johnson", "vaccines", "vaccine", "mandates", "mandate"]
    # items_keywords = ["mask", "masks", "n95", "hand sanitizer", "toilet paper"] 

    # final_keywords = covid_keywords + variants_keywords + pandemic_keywords + vaccine_keywords + items_keywords 

    return covid_keywords 

def get_dates():
    """
    Gets a list of dates that we want to provide the search query for. 
    returns: begin_dates, end_dates, months 
    """

    # Beginning dates 
    begin_dates_2020 = ["2020-01-01", "2020-02-01", "2020-03-01", "2020-04-01", "2020-05-01", "2020-06-01", "2020-07-01", "2020-08-01", "2020-09-01", "2020-10-01", "2020-11-01", "2020-12-01"]
    begin_dates_2021 = ["2021-01-01", "2021-02-01", "2021-03-01", "2021-04-01", "2021-05-01", "2021-06-01", "2021-07-01", "2021-08-01", "2021-09-01", "2021-10-01", "2021-11-01", "2021-12-01"]
    begin_dates = {"2020": begin_dates_2020, "2021": begin_dates_2021}

    # Ending dates 
    end_dates_2020 = ["2020-01-31", "2020-02-28", "2020-03-31", "2020-04-30", "2020-05-31", "2020-06-30", "2020-07-31", "2020-08-31", "2020-09-30", "2020-10-31", "2020-11-30", "2020-12-31"]
    end_dates_2021 = ["2021-01-31", "2021-02-28", "2021-03-31", "2021-04-30", "2021-05-31", "2021-06-30", "2021-07-31", "2021-08-31", "2021-09-30", "2021-10-31", "2021-11-30", "2021-12-31"]
    end_dates = {"2020": end_dates_2020, "2021": end_dates_2021}

    # Months 
    months_2020 = {"2020-01": "January 2020", "2020-02": "February 2020", "2020-03": "March 2020", "2020-04":"April 2020", "2020-05": "May 2020", "2020-06": "June 2020", "2020-07": "July 2020", "2020-08": "August 2020", "2020-09": "September 2020", "2020-10": "October 2020", 
    "2020-11" : "November 2020", "2020-12" : "December 2020"}

    months_2021 = {"2021-01": "January 2021", "2021-02": "February 2021", "2021-03": "March 2021", "2021-04":"April 2021", "2021-05": "May 2021", "2021-06": "June 2021", "2021-07": "July 2021", "2021-08": "August 2021", "2021-09": "September 2021", "2021-10": "October 2021", 
    "2021-11" : "November 2021", "2021-12" : "December 2021"}

    months_mapping = months_2020 | months_2021 

    return begin_dates, end_dates, months_mapping

def main(): 
    
    final_keywords = get_covid_keywords()
    begin_dates, end_dates, months_mapping = get_dates() 

    # scrape_tweets("FoxNews", final_keywords, begin_dates["2020"], end_dates["2020"])
    # scrape_tweets("CNN", final_keywords, begin_dates["2020"], end_dates["2020"])

    # scrape_tweets("FoxNews", final_keywords, begin_dates["2021"], end_dates["2021"])
    # scrape_tweets("CNN", final_keywords, begin_dates["2021"], end_dates["2021"])

    dirty_path = './data_dirty/cnn_tweets_2020_dirty.jsonl'
    clean_path = './data_clean/cnn_tweets_2020_clean.json'
    parse_jsonl_file(dirty_path, clean_path, months_mapping)

if __name__ == "__main__":
    main() 