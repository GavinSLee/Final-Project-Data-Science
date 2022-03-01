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
]

# Months 
months_2020 = {"2020-01": "January 2020", "2020-02": "February 2020", "2020-03": "March 2020", "2020-04":"April 2020", "2020-05": "May 2020", "2020-06": "June 2020", "2020-07": "July 2020", "2020-08": "August 2020", "2020-09": "September 2020", "2020-10": "October 2020", 
"2020-11" : "November 2020", "2020-12" : "December 2020"}

months_2021 = {"2021-01": "January 2021", "2021-02": "February 2021", "2021-03": "March 2021", "2021-04":"April 2021", "2021-05": "May 2021", "2021-06": "June 2021", "2021-07": "July 2021", "2021-08": "August 2021", "2021-09": "September 2021", "2021-10": "October 2021", 
"2021-11" : "November 2021", "2021-12" : "December 2021"}

months_mapping = months_2020 | months_2021 

def get_tweets_from_json(path):
  with open(path, ) as f:
    tweets = json.load(f)
    return tweets

def save_tweets_to_json(path, tweets):
  with open(path, 'w') as outfile:
      json.dump(tweets, outfile)
      print("Saved to " + path)

def remove_duplicate_tweets():
  # TODO: remove duplicate tweets
  pass

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

    
def main():
  JSON_FILE = "cnn_tweets_2020_clean.json"
  ROOT = "../data_clean/"
  PATH = ROOT + JSON_FILE
  tweets = get_tweets_from_json(PATH)
  tweets = assign_keywords(tweets)
  save_tweets_to_json("preprocessing.json", tweets)


if __name__ == "__main__":
    main() 


        
      

