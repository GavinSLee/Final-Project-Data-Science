from asyncio.proactor_events import _ProactorWritePipeTransport
from json.tool import main
import json 
import os 

"""
This file is responsible for scraping covid related tweets from CNN and Fox News from January 2020 - December 2021. We use the library snscrape to gather the tweets, and this library simplifies our work by no longer needing to use a web browser based scraper (like selenium) to gather the tweets. All scraped data is written to cnn_tweets.json and fox_tweets.json. 

To run this file, use the command: python news_tweets.py in your shell. 
"""

# 1. Define COVID related keywords to pass to our search query. 
COVID_KEYWORDS = ["coronavirus", "covid", "covid19", "covid-19", "sarscov2", "sars cov 2", "wuhan"]
VARIANTS_KEYWORDS = ["delta", "delta variant", "omicron", "omicron variant", "variant"]
PANDEMIC_KEYWORDS = ["pandemic", "quarantine", "self-quarantine", "self quarantine", "self-isolation", "self isolation", "lockdown", "social distancing", "flattening the curve", "flatten the curve", "herd immunity", "sympatomatic", "asymptomatic"] 
VACCINE_KEYWORDS = ["moderna", "Pfizer", "johnson & johnson", "vaccine"]
ITEMS_KEYWORDS = ["nasks", "n95", "hand sanitizer", "toilet paper"] 
PEOPLE_KEYWORDS = ["trump", "fauci", "biden", "harris"]

FINAL_KEYWORDS = COVID_KEYWORDS + VARIANTS_KEYWORDS + PANDEMIC_KEYWORDS + VACCINE_KEYWORDS + ITEMS_KEYWORDS

# 2. Define news outlets from which we want to scrape covid related tweets from. 
NEWS_OUTLETS = ["FoxNews", "CNN"]

# 3. Define beginning and ending dates to pass to our search query.  
BEGINNING_DATES_2020 = ["2020-01-01", "2020-02-01", "2020-03-01", "2020-04-01", "2020-05-01", "2020-06-01", "2020-07-01", "2020-08-01", "2020-09-01", "2020-10-01", "2020-11-01", "2020-12-01"]
END_DATES_2020 = ["2020-01-31", "2020-02-28", "2020-03-31", "2020-04-30", "2020-05-31", "2020-06-30", "2020-07-31", "2020-08-31", "2020-09-30", "2020-10-31", "2020-11-30", "2020-12-31"]
BEGINNING_DATES_2021 = ["2021-01-01", "2021-02-01", "2021-03-01", "2021-04-01", "2021-05-01", "2021-06-01", "2021-07-01", "2021-08-01", "2021-09-01", "2021-10-01", "2021-11-01", "2021-12-01"]
END_DATES_2021 = ["2021-01-31", "2021-02-28", "2021-03-31", "2021-04-30", "2021-05-31", "2021-06-30", "2021-07-31", "2021-08-31", "2021-09-30", "2021-10-31", "2021-11-30", "2021-12-31"]

def scrape_tweets(keywords, news_outlets, beginning_dates, end_dates):


    # We gather tweets per month. 
    for i in range(len(beginning_dates)):
        begin_date = beginning_dates[i] 
        end_date = end_dates[i] 

        # Snscrape uses a CLI command to scrape tweets. The parameters --jsonl writes the scraped data to a json file, and --progress prints scraped data progress. 
        base_command = "snscrape --jsonl --progress --max-results 1000 --since " + begin_date + " twitter-search "

        # Gather covid related tweets per our defined keywords, for each news outlet. 
        for outlet in news_outlets: 
            for keyword in keywords:
                query = keyword + " "
                news_outlet = "from:" + outlet + " "
                until = "until:" + end_date 
                if outlet == "CNN":
                    output = " >> " + "test_tweets.jsonl"
                else:
                    output = " >> " + "test_tweets.jsonl"

                search_command = "\"" + query + news_outlet + until + "\""
                final_command = base_command + search_command + output 
                print(final_command) 
                os.system(final_command) 

# Need to do some preprocessing as there's too much information 
def clean_jsonl_file(dirty_path, clean_path):
    with open(dirty_path, 'r') as f:
        json_list = list(f)

    clean_tweets = {"tweets": []}    
    keys_to_remove = ["_type", "user", "source", "sourceUrl", "sourceLabel", "outlinks", "tcooutlinks"]    
    for json_str in json_list:
        curr_tweet = json.loads(json_str) 
        for key in keys_to_remove:
            curr_tweet.pop(key)
        clean_tweets["tweets"].append(curr_tweet) 
    
    with open(clean_path, 'w') as f:
        json.dump(clean_tweets, f) 

def clean_files():
    dirty_paths = ['./data_dirty/fox_tweets.jsonl', './data_dirty/cnn_tweets.jsonl']
    clean_paths = ['./data_clean/fox_tweets.json', './data_clean/cnn_tweets.json']

    for i in range(len(dirty_paths)):
        curr_dirty_path = dirty_paths[i] 
        curr_clean_path = clean_paths[i] 
        clean_jsonl_file(curr_dirty_path, curr_clean_path)

    print("Cleaning Finished.")

def main(): 
    # scrape_tweets(FINAL_KEYWORDS, NEWS_OUTLETS, BEGINNING_DATES_2021, END_DATES_2021)
    clean_files() 

if __name__ == "__main__":
    main() 