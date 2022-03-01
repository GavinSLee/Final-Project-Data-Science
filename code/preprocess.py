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


        
      

