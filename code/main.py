from json.tool import main
import requests
import os 
import json  
import snscrape
import pandas as pd 

# 1. Define COVID related keywords to pass to our search query. 
COVID_KEYWORDS = ["coronavirus", "corona", "covid", "covid19", "covid-19", "sarscov2", "sars cov 2", "chinese virus", "wuhan virus"]
PANDEMIC_KEYWORDS = ["pandemic", "quarantine", "self-quarantine", "self quarantine", "self-isolation", "self isolation", "lockdown", "social distancing", "flattening the curve", "flatten the curve", "herd immunity", "sympatomatic", "asymptomatic"] 
PEOPLE_KEYWORDS = ["Trump", "Fauci", "Biden", "Harris"]
VACCINE_KEYWORDS = ["Moderna", "Pfizer", "Johnson & Johnson", "Vaccine"]
ITEMS_KEYWORDS = ["Masks", "n95", "hand sanitizer", "toilet paper"] 

FINAL_KEYWORDS = COVID_KEYWORDS + PANDEMIC_KEYWORDS + PEOPLE_KEYWORDS + VACCINE_KEYWORDS + ITEMS_KEYWORDS 

NEWS_OUTLETS = ["FoxNews", "CNN"]

FILE = "news_outlets_tweets.json"

# 2. Create beginning and ending dates to pass to our search query.  
BEGINNING_DATES_2020 = ["2020-01-01", "2020-02-01", "2020-03-01", "2020-04-01", "2020-05-01", "2020-06-01", "2020-07-01", "2020-08-01", "2020-09-01", "2020-10-01", "2020-11-01", "2020-12-01"]
END_DATES_2020 = ["2020-01-31", "2020-02-28", "2020-03-31", "2020-04-30", "2020-05-31", "2020-06-30", "2020-07-31", "2020-08-31", "2020-09-30", "2020-10-31", "2020-11-30", "2020-12-31"]
BEGINNING_DATES_2021 = ["2021-01-01", "2021-02-01", "2021-03-01", "2021-04-01", "2021-05-01", "2021-06-01", "2021-07-01", "2021-08-01", "2021-09-01", "2021-10-01", "2021-11-01", "2021-12-01"]
END_DATES_2021 = ["2021-01-31", "2021-02-28", "2021-03-31", "2021-04-30", "2021-05-31", "2021-06-30", "2021-07-31", "2021-08-31", "2021-09-30", "2021-10-31", "2021-11-30", "2021-12-31"]

def scrape_tweets(keywords, news_outlets, beginning_dates, end_dates, file):
    base_command = "snscrape --jsonl --progress --max-results 1000 twitter-search "

    for i in range(len(beginning_dates)):
        begin_date = beginning_dates[i] 
        end_date = end_dates[i] 
        for outlet in news_outlets: 
            for keyword in keywords:
                query = keyword + " "
                news_outlet = "from:" + outlet + " "
                since = "since:" + begin_date + " "
                until = "until:" + end_date 
                output = " >> " + file 

                search_command = "\"" + query + news_outlet + since + until + "\""
                final_command = base_command + search_command + output 
                print(final_command) 
                os.system(final_command) 

if __name__ == "__main__":
    scrape_tweets(COVID_KEYWORDS, NEWS_OUTLETS, BEGINNING_DATES_2020, END_DATES_2020, FILE)


# Search queries from Tweets Research Paper: corona, #corona, coronavirus, #coronavirus, covid, #covid, covid19, #covid19, covid-19, #covid-19, sarscov2, #sarscov2, sars cov2, sars cov 2, covid_19, #covid_19, #ncov, ncov, #ncov2019, ncov2019, 2019-ncov, #2019-ncov, pandemic, #pandemic #2019ncov, 2019ncov, quarantine, #quarantine, flatten the curve, flattening the curve, #flatteningthecurve, #flattenthecurve, hand sanitizer, #handsanitizer, #lockdown, lockdown, social distancing, #socialdistancing, work from home, #workfromhome, working from home, #workingfromhome, ppe, n95, #ppe, #n95, #covidiots, covidiots, herd immunity, #herdimmunity, pneumonia, #pneumonia, chinese virus, #chinesevirus, wuhan virus, #wuhanvirus, kung flu, #kungflu, wearamask, #wearamask, wear a mask, vaccine, vaccines, #vaccine, #vaccines, corona vaccine, corona vaccines, #coronavaccine, #coronavaccines, face shield, #faceshield, face shields, #faceshields, health worker, #healthworker, health workers, #healthworkers, #stayhomestaysafe, #coronaupdate, #frontlineheroes, #coronawarriors, #homeschool, #homeschooling, #hometasking, #masks4all, #wfh, wash ur hands, wash your hands, #washurhands, #washyourhands, #stayathome, #stayhome, #selfisolating, self isolating 