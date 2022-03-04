from json.tool import main
import os 

"""
This file is responsible for scraping covid related tweets from CNN and Fox News from January 2020 - December 2021. We use the library snscrape to gather the tweets, and this library simplifies our work by no longer needing to use a web browser based scraper (like selenium) to gather the tweets. 

The data is first written as jsonl (json lines) files in the directory: data_dirty. Then, we parse through the files, removing some unnecessary attributes. We write the clean data as json files to data_clean.  

To run this file, use the command: python code/news_tweets.py in your shell. 
"""

def scrape_tweets(news_outlet, path, keywords, max_result, begin_dates, end_dates):
    """
    This is the main method that scrapes tweets using the snscrape library. The snscrape library mainly uses a CLI; however, we can make use of python's OS package to scrape more programmatically. We iterate by month. 

    :param news_outlet: string (news outlet we want to scrape for)
    :param keywords: list (keywords that we want to base our search query off of)
    :param begin_dates: list (list of the first of each month that we want to search off of)
    :param end_dates: list (list of the end of each month that we want to search off of)
    :param months: list (what month we're searching for)

    :returns: None (writes the parsed result to a file in the ./data_clean directory)
    """
    
    
    # Delete contents of file first 
    f = open(path, "w")
    f.truncate() 
    f.close() 

    # We gather tweets per month. 
    for i in range(len(begin_dates)):
        begin_date = begin_dates[i] 
        end_date = end_dates[i] 

        # Snscrape uses a CLI command to scrape tweets. The parameters --jsonl writes the scraped data to a json file, and --progress prints scraped data progress. 
        base_command = "snscrape --jsonl --progress --max-results " + max_result + " --since " + begin_date + " twitter-search "
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

def main(): 

    # Begin dates 
    begin_dates_2020 = ["2020-01-01", "2020-02-01", "2020-03-01", "2020-04-01", "2020-05-01", "2020-06-01", "2020-07-01", "2020-08-01", "2020-09-01", "2020-10-01", "2020-11-01", "2020-12-01"]
    begin_dates_2021 = ["2021-01-01", "2021-02-01", "2021-03-01", "2021-04-01", "2021-05-01", "2021-06-01", "2021-07-01", "2021-08-01", "2021-09-01", "2021-10-01", "2021-11-01", "2021-12-01"]

    # Ending dates 
    end_dates_2020 = ["2020-01-31", "2020-02-28", "2020-03-31", "2020-04-30", "2020-05-31", "2020-06-30", "2020-07-31", "2020-08-31", "2020-09-30", "2020-10-31", "2020-11-30", "2020-12-31"]
    end_dates_2021 = ["2021-01-31", "2021-02-28", "2021-03-31", "2021-04-30", "2021-05-31", "2021-06-30", "2021-07-31", "2021-08-31", "2021-09-30", "2021-10-31", "2021-11-30", "2021-12-31"]

    # Final Parameters to pass to snscrape calls 
    COVID_KEYWORDS = ["coronavirus", "corona virus", "corona", "covid", "covid19", "covid-19", "covid 19", "sarscov2", "sars cov 2", "wuhan virus"]
    BEGIN_DATES = begin_dates_2020 + begin_dates_2021
    END_DATES = end_dates_2020 + end_dates_2021 

    FOX_PATH = '../data_dirty/fox_tweets_dirty.jsonl'
    CNN_PATH = '../data_dirty/cnn_tweets_dirty.jsonl'

    FOX_MAX_RESULT = "1000"
    CNN_MAX_RESULT = "50"

    scrape_tweets("FoxNews", FOX_PATH, COVID_KEYWORDS, FOX_MAX_RESULT, BEGIN_DATES, END_DATES)
    scrape_tweets("CNN", CNN_PATH, COVID_KEYWORDS, CNN_MAX_RESULT, BEGIN_DATES, END_DATES)

if __name__ == "__main__":
    main() 