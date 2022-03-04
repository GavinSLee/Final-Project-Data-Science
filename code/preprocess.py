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
  "mask",
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

  #additional health words:
  "hospital",
  "surgery",
  "respirator",
  "emergency room",
  "emergency",
  

  #politics
  "biden", 
  "trump",
  "white house", 
  "CDC", 
  "Center for Disease Control"
  "WHO", 
  "World Health Organization", 
  "shutdown",
  "lockdown",
  "restrictions",
  "democrat",
  "republican",
  "GOP",
  "Dem",
  "senate",
  "house",
  "house of representatives",
  "harris",
  "pelosi",
  "romney",
  "sanders",
  "Boris Johnson",
  "cuomo",
  "fox",
  "cnn", 
  "fauci"


  

  #transportations
  "Airport", 
  "Bus", 
  "Public Transportation", 
  "Ship", 
  "Cruise",
  "airplane",
  "airline",
  
  #Location
  "USA",
  "United States",
  "New York", 
  "Rhode Island", 
  "Massachusetts", 
  "California", 
  "Texas", 
  "Guam",
  "Boston", 
  "New York", 
  "Los Angeles",
  "Connecticut",
  "Rhode Island",
  "Pennsylvania", 
  "Georgia", 
  "Atlanta", 
  "UK", 
  "United Kingdom", 
  "Germany", 
  "Australia",
  "China", 
  "Beijing", 
  "Taiwan", 
  "Wuhan", 
  "Japan", 
  "India",
  "Tokyo",
  "South Africa", 
  "South Korea", 
  "North Korea", 
  "Vietnam", 
  "EU", 
  "European Union",
  "Russia", 
  'Brittain',

  #market related
  "Stock",
  "Supply Chain",
  "Inflation",
  "Deflation",
  "Market",
  "Wall Street",
  "economy",
  "currency",
  "commerce",

  #vaccine related
  "pfizer",
  "moderna",
  "jnj"
  "johnson and johnson",
  "booster",
  "dose",
  "first dose",
  "second dose",
  "research", 

  #variants
  "omicron", 
  "delta", 

  #symptoms
  "positive",
  "negative",
  "cough",
  "vomit",
  "headache",
  "nausea",
  

  #religion
  "chirstian",
  "religion",
  "religious",
  "bible",


  #other terms
  "fake news",
  "death",
  "casualty",
  "death toll",
  

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
  id = set()
  unique_tweets = []
  for tweet in tweets:
    if tweet["id"] not in id:
      unique_tweets.append(tweet)
      id.add(tweet["id"])
  return unique_tweets

def assign_keywords(tweets):
  for tweet in tweets:
    content = tweet["text"].lower()
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

def convert_news_jsonl_to_json(read_path, save_path):
  """
  Cleans up a dirty news tweets jsonl file and writes the data to a clean json file. 
  """

  with open(read_path, 'r') as f:
      json_list = list(f) 

  tweets_list = []
  for json_str in json_list:
      json_line = json.loads(json_str) 
      username = json_line["user"]["displayname"]
      author_id = json_line["user"]["id"]
      json_line["news_outlet"] = username 
      json_line["author_id"] = str(author_id) 
      json_line["id"] = str(json_line["id"])
      conversation_id = str(json_line["conversationId"])
      json_line["conversation_id"] = conversation_id
      text = json_line["content"]
      json_line["text"] = text 
      reply_count = json_line["replyCount"]
      json_line["reply_count"] = reply_count
      retweet_count = json_line["retweetCount"]
      json_line["retweet_count"] = retweet_count 
      like_count = json_line["likeCount"]
      json_line["like_count"] = like_count
      quote_count = json_line["quoteCount"]
      json_line["quote_count"] = quote_count
      
      json_line = add_month(json_line) 
      json_line = remove_keys(json_line)
      tweets_list.append(json_line) 
  
  with open(save_path, 'w') as f:
      json.dump(tweets_list, f) 

def remove_keys(json_line):
  """
  Removes unnecessary fields from the JSONL lines. 
  """

  keys_to_remove = ["_type", "conversationId", "content", "replyCount", "retweetCount", "likeCount", "quoteCount", "user", "source", "sourceUrl", "sourceLabel", "tcooutlinks", "media", "retweetedTweet", "quotedTweet", "inReplyToTweetId", "inReplyToUser", "mentionedUsers", "coordinates", "place", "cashtags", "renderedContent"]
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

def parse_clean_news_tweets_file(read_path, save_path):
  """
  These are the functions Andrew wrote to remove duplicate tweets and assign keywords. 
  """
  tweets = get_tweets_from_json(read_path)
  tweets = remove_duplicate_tweets(tweets)
  tweets = assign_keywords(tweets)
  save_tweets_to_json(save_path, tweets)


def preprocess_news_tweets_files_final():
  """
  This funciton does all of the final preprocessing for the news tweets files.
  """
  fox_tweets_dirty_path = "../data_dirty/fox_tweets_dirty.jsonl"
  fox_tweets_clean_path = "../data_clean/fox_tweets_clean.json"

  cnn_tweets_dirty_path = "../data_dirty/cnn_tweets_dirty.jsonl"
  cnn_tweets_clean_path = "../data_clean/cnn_tweets_clean.json"

  convert_news_jsonl_to_json(fox_tweets_dirty_path, fox_tweets_clean_path)
  convert_news_jsonl_to_json(cnn_tweets_dirty_path, cnn_tweets_clean_path)

  parse_clean_news_tweets_file(fox_tweets_clean_path, fox_tweets_clean_path)
  parse_clean_news_tweets_file(cnn_tweets_clean_path, cnn_tweets_clean_path)


def convert_replies_jsonl_to_json(dirty_path, clean_path):
  """
  Converts the replies jsonl file to a json file. 
  """

  with open(dirty_path, 'r') as f:
    json_list = list(f)
  
  replies_list = []
  for json_str in json_list:
    json_line = json.loads(json_str) 
    replies_list.append(json_line)
  
  with open(clean_path, 'w') as f:
    json.dump(replies_list, f) 

def check_replies_conversation_ids(news_tweets_path, replies_clean_path):

  """
  Determines whether there are any tweets where the conversation id is not a news tweet id. 
  """

  with open(news_tweets_path, 'r') as f:
    news_tweets_list = json.load(f)

  tweets_id_map = {} 
  for tweet in news_tweets_list:
    id = tweet["id"]
    if id not in tweets_id_map:
      tweets_id_map[id] = 1

  valid_replies = [] 
  with open(replies_clean_path, 'r') as f:
    replies_list = json.load(f)  
  
  for reply in replies_list:
    conversation_id = reply["conversation_id"]
    if conversation_id in tweets_id_map:
      valid_replies.append(reply) 
  
  with open(replies_clean_path, 'w') as f:
    json.dump(valid_replies, f)

def replies_add_fields(news_outlet, replies_clean_path):
  """
  Adds news outlet and date field for reference purposes. 
  """
  with open(replies_clean_path, 'r') as f:
    replies_list = json.load(f) 
  
  final_replies = [] 
  for reply in replies_list: 
    reply["news_outlet"] = news_outlet
    date = reply["created_at"] 
    reply["date"] = date
    reply.pop("created_at")
    final_replies.append(reply) 
  
  with open(replies_clean_path, 'w') as f:
    json.dump(final_replies, f) 

def preprocess_replies_tweets_files_final():
  """
  This method does all the final preprocessing, to be called in main(). 
  """
  fox_replies_dirty_path = "../data_dirty/fox_replies_dirty.jsonl"
  fox_replies_clean_path = "../data_clean/fox_replies_clean.json"
  fox_tweets_clean_path = "../data_clean/fox_tweets_clean.json"

  cnn_replies_dirty_path = "../data_dirty/cnn_replies_dirty.jsonl"
  cnn_replies_clean_path = "../data_clean/cnn_replies_clean.json"
  cnn_tweets_clean_path = "../data_clean/cnn_tweets_clean.json"

  convert_replies_jsonl_to_json(fox_replies_dirty_path, fox_replies_clean_path)
  convert_replies_jsonl_to_json(cnn_replies_dirty_path, cnn_replies_clean_path)

  check_replies_conversation_ids(fox_tweets_clean_path, fox_replies_clean_path)
  check_replies_conversation_ids(cnn_tweets_clean_path, cnn_replies_clean_path)

  replies_add_fields("Fox News", fox_replies_clean_path)
  replies_add_fields("CNN", cnn_replies_clean_path)

def create_sample_file(read_path, write_path): 
  with open(read_path, 'r') as f:
    data_list = json.load(f) 
  
  sample = [] 
  for i in range(120):
    curr_data = data_list[i] 
    sample.append(curr_data) 
  
  with open(write_path, 'w') as f:
    json.dump(sample, f) 
  
def create_samples():
  fox_tweets_clean_path = "../data_clean/fox_tweets_clean.json"
  fox_tweets_sample_path = "../data_samples/fox_tweets_sample.json"

  fox_replies_clean_path = "../data_clean/fox_replies_clean.json"
  fox_replies_sample_path = "../data_samples/fox_replies_sample.json"

  
  cnn_tweets_clean_path = "../data_clean/cnn_tweets_clean.json"
  cnn_tweets_sample_path = "../data_samples/cnn_tweets_sample.json"

  cnn_replies_clean_path = "../data_clean/cnn_replies_clean.json"
  cnn_replies_sample_path = "../data_samples/cnn_replies_sample.json"

  create_sample_file(fox_tweets_clean_path, fox_tweets_sample_path)
  create_sample_file(fox_replies_clean_path, fox_replies_sample_path)
  create_sample_file(cnn_tweets_clean_path, cnn_tweets_sample_path)
  create_sample_file(cnn_replies_clean_path, cnn_replies_sample_path)

def main():
  # preprocess_news_tweets_files_final() 
  # preprocess_replies_tweets_files_final() 
  create_samples() 
  
if __name__ == "__main__":
    main() 


        
      

