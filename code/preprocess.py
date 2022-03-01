import json

terms = [
  "aerosol", 
  "antibody", 
  "antibody test",
  "antigen test",
  "asymptomatic"
  "contact tracing",
  "convalescent plasma therapy",
  "diagnostic test",
  "drive-thru testing",

  # TODO: get as many terms as you can!!!
  # 
]



def get_tweets_from_json(path):
  with open(path, ) as f:
    tweets = json.load(f)
    return tweets

def save_tweets_to_json(path, tweets):
  with open(path, 'w') as outfile:
      json.dump(tweets, outfile)
      print("Saved to " + path)

def assign_keywords(tweets):
  for tweet in tweets:
    content = tweet["content"].lower()
    keywords = []
    for term in terms:
      term = term.lower()
      firstIndex = 0
      lastIndex = len(term)
      for i in range(len(content) - lastIndex):
        substring = content[i + firstIndex : i + lastIndex]
        if substring == term:
          keywords.append(term)
    tweet["keywords"] = keywords
  return tweets

    
def main():
  JSON_FILE = "cnn_tweets_2020_clean.json"
  ROOT = "../data_clean/"
  PATH = ROOT + JSON_FILE
  tweets = get_tweets_from_json(PATH)
  tweets = assign_keywords(tweets)
  save_tweets_to_json("preprocessing.json", tweets)


if __name__ == "__main__":
    main() 


        
      

