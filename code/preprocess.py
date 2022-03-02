from enum import unique
import json

terms = [
  # these covid related terms are from here: https://www.webmd.com/lung/coronavirus-glossary#5
  "aerosol", 
  "antibody", 
  "antibody test",
  "antigen test",
  "asymptomatic"
  "contact tracing",
  "convalescent plasma therapy",
  "diagnostic test",
  "drive-thru testing",
  "droplet",
  "emergency use authorization",
  "endemic",
  "Epidemic",
  "Flattening the curve",
  "Herd immunity",
  "Hydroxychloroquine",
  "Incubation period",
  "Infusion",
  "N95 respirator",
  "N95",
  "N95 mask",
  "Outbreak",
  "Pandemic",
  "Paxlovid",
  "PCR test",
  "PCR",
  "Personal protective equipment",
  "PPE",
  "Pre-symptomatic",
  "Quarantine",
  "R0",
  "Remdesivir",
  "Veklury",
  "Self-isolation",
  "Serology test",
  "Social distancing",
  "State of emergency",
  "Swab test",
  "Tocilizumab",
  "Actemra",
  "Trial",
  "Vaccine",
  "Variant",
  "Ventilator",
  "Viral load",
  "Viral shedding",
  "Viral test",

  # TODO: get as many terms as you can!!!
  # For instance, political words like Biden / Trump, organizations like CDC, etc

  #politics
  "biden", 
  "trump",
  "white house", 
  "CDC", 
  "Center for Disease Control"
  "WHO", 
  "World Health Organization", 

  #transportations
  "Airport", 
  "Bus", 
  "Public Transportation", 
  
  #Location
  "USA",
  "United States",
  "UK", 
  "United Kingdom", 
  "Germany", 
  "Australia",
  "China", 
  "Wuhan"

]

def get_tweets_from_json(path):
  with open(path, ) as f:
    tweets = json.load(f)
    return tweets

def save_tweets_to_json(path, tweets):
  with open(path, 'w') as outfile:
      json.dump(tweets, outfile)
      print("Saved to " + path)

def remove_duplicate_tweets(tweets):
  # TODO: remove duplicate tweets
  id = set()
  unique_tweets = []
  for tweet in tweets:
    if tweet["id"] not in id:
      unique_tweets.append(tweet)
      id.add(tweet["id"])
  return unique_tweets

def assign_keywords(tweets):
  for tweet in tweets:
    content = tweet["content"].lower()
    keywords = set()
    for term in terms:
      term = term.lower()
      firstIndex = 0
      lastIndex = len(term)
      for i in range(len(content) - lastIndex):
        substring = content[i + firstIndex : i + lastIndex]
        if substring == term:
          keywords.add(term)
    tweet["keywords"] = list(keywords)
  return tweets

def clean_replies_jsonl_file(read_path, save_path):
  """
  Cleans up a dirty replies jsonl file and writes the data to a clean json file. 
  """
  with open(read_path, 'r') as read_json_file:
    json_list = list(read_json_file)
  
  replies_list = [] 
  for json_str in json_list:
    json_line = json.loads(json_str) 
    replies_list.append(json_line)
  
  with open(save_path, 'w') as save_json_file:
    json.dump(replies_list, save_json_file) 

def clean_news_tweet_jsonl_file(read_path, save_path):
  """
  Cleans up a dirty news tweets jsonl file and writes the data to a clean json file. 
  """

  with open(read_path, 'r') as read_json_file:
      json_list = list(read_json_file) 

  tweets_list = []
  for json_str in json_list:
      json_line = json.loads(json_str) 
      username = json_line["user"]["displayname"]
      author_id = json_line["user"]["id"]
      json_line["username"] = username 
      json_line["author_id"] = author_id 
      json_line = add_month(json_line) 
      json_line = remove_keys(json_line)
      tweets_list.append(json_line) 
  
  with open(save_path, 'w') as save_json_file:
      json.dump(tweets_list, save_json_file) 

def remove_keys(json_line):
  """
  Removes unnecessary fields from the JSONL lines. 
  """

  keys_to_remove = ["_type", "user", "source", "sourceUrl", "sourceLabel", "tcooutlinks", "media", "retweetedTweet", "quotedTweet", "inReplyToTweetId", "inReplyToUser", "mentionedUsers", "coordinates", "place", "cashtags", "renderedContent"]
  for key in keys_to_remove:
    json_line.pop(key)
  return json_line 

def add_month(json_line):
  """
  Adds a month field for easier analysis later on. 
  """

  months_2020 = {"2020-01": "January 2020", "2020-02": "February 2020", "2020-03": "March 2020", "2020-04":"April 2020", "2020-05": "May 2020", "2020-06": "June 2020", "2020-07": "July 2020", "2020-08": "August 2020", "2020-09": "September 2020", "2020-10": "October 2020", 
  "2020-11" : "November 2020", "2020-12" : "December 2020"}

  months_2021 = {"2021-01": "January 2021", "2021-02": "February 2021", "2021-03": "March 2021", "2021-04":"April 2021", "2021-05": "May 2021", "2021-06": "June 2021", "2021-07": "July 2021", "2021-08": "August 2021", "2021-09": "September 2021", "2021-10": "October 2021", 
  "2021-11" : "November 2021", "2021-12" : "December 2021"}

  months_mapping = months_2020 | months_2021 
  date = json_line["date"]
  date = date[0:7] 
  json_line["month"] = months_mapping[date]
  return json_line 

def parse_news_tweet_files():
  fox_read_path = "./data_dirty/fox_tweets_dirty.jsonl"
  fox_write_path = "./data_clean/fox_tweets_clean.json"
  clean_news_tweet_jsonl_file(fox_read_path, fox_write_path) 

  cnn_read_path = "./data_dirty/cnn_tweets_dirty.jsonl"
  cnn_write_path = "./data_clean/cnn_tweets_clean.json"
  clean_news_tweet_jsonl_file(cnn_read_path, cnn_write_path)


def main():

  # parse_news_tweet_files() 

  # raw json we are reading in 
  READ_PATH = "../data_clean/cnn_tweets_clean.json"

  # where we are storing preprocessed json
  SAVE_PATH = "new_preprocessing.json"

  tweets = get_tweets_from_json(READ_PATH)
  tweets = remove_duplicate_tweets(tweets)
  tweets = assign_keywords(tweets)
  save_tweets_to_json(SAVE_PATH, tweets)


if __name__ == "__main__":
    main() 


        
      

