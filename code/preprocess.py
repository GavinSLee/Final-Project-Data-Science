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

    
def main():
  #raw json we are reading in 
  READ_PATH = "../data_clean/cnn_tweets_2020_clean.json"

  #where we are storing preprocessed json
  SAVE_PATH = "new_preprocessing.json"

  tweets = get_tweets_from_json(READ_PATH)
  tweets = remove_duplicate_tweets(tweets)
  tweets = assign_keywords(tweets)
  save_tweets_to_json(SAVE_PATH, tweets)


if __name__ == "__main__":
    main() 


        
      

