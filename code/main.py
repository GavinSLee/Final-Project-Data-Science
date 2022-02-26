from json.tool import main
import requests
import os 
import json  
import snscrape
import pandas as pd 

# 1. Define COVID related keywords to pass to our search query. 
COVID_KEYWORDS = ["coronavirus", "covid", "covid19", "covid-19", "sarscov2", "sars cov 2", "wuhan"]
PANDEMIC_KEYWORDS = ["pandemic", "quarantine", "self-quarantine", "self quarantine", "self-isolation", "self isolation", "lockdown", "social distancing", "flattening the curve", "flatten the curve", "herd immunity", "sympatomatic", "asymptomatic"] 
VACCINE_KEYWORDS = ["moderna", "Pfizer", "johnson & johnson", "vaccine"]
ITEMS_KEYWORDS = ["nasks", "n95", "hand sanitizer", "toilet paper"] 
PEOPLE_KEYWORDS = ["trump", "fauci", "biden", "harris"]

FINAL_KEYWORDS = COVID_KEYWORDS + PANDEMIC_KEYWORDS + VACCINE_KEYWORDS + ITEMS_KEYWORDS 

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
                    output = " >> " + "cnn_tweets.json"
                else:
                    output = " >> " + "fox_tweets.json"

                search_command = "\"" + query + news_outlet + until + "\""
                final_command = base_command + search_command + output 
                print(final_command) 
                os.system(final_command) 
                # return 

if __name__ == "__main__":
    scrape_tweets(FINAL_KEYWORDS, NEWS_OUTLETS, BEGINNING_DATES_2021, END_DATES_2021)
