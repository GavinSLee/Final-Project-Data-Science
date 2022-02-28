import requests
import os
import json
import pandas as pd 

# To set your enviornment variables in your terminal run the following line:
bearer_token = "AAAAAAAAAAAAAAAAAAAAABtGZgEAAAAAa7ycbW8F%2FKadNlE8SvMkZJgjxK0%3DHLQ6jNZL9RAA5zjAdEJxZT7X2bJZoDAXZvNaYC2VmR7SnEItxj"

def create_url():
    tweet_fields = "tweet.fields=lang,author_id"
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    ids = "ids=1278747501642657792,1255542774432063488"
    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated IDs
    url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def get_ids(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
        # Gets list of tweets from path 
        tweets = data["tweets"]
    
    ids = []
    for tweet in tweets:
        id = tweet["id"]
        ids.append(id) 
    return ids 

def main():
    # url = create_url()
    # json_response = connect_to_endpoint(url)
    # print(json.dumps(json_response, indent=4, sort_keys=True))
    json_path = './data_clean/fox_tweets.json'
    ids = get_ids(json_path) 

if __name__ == "__main__":
    main()