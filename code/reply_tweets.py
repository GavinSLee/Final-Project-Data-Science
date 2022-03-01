import snscrape 
import json 
import subprocess
import requests
import time 

# To set your enviornment variables in your terminal run the following line:
bearer_token = "AAAAAAAAAAAAAAAAAAAAABtGZgEAAAAADeKNHec%2Fs72Q33f6h8ng1yo4CYE%3DrKlRJ3KY0a2IHWJVQDnTJGoG6osF1QpYi95pDqoxBipEJz6kwf"

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r

def create_url(id):
    """
    Creates the URL endpoint to gather our data from. 
    """
    tweet_fields = "tweet.fields=lang,author_id,conversation_id,public_metrics"
    ids = "ids=" + id 
    url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
    return url

def connect_to_endpoint(url):
    """
    Gets response from the endpoint. 
    """
    response = requests.request("GET", url, auth=bearer_oauth)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

# def create_news_tweets_dict(clean_path):
#     """
#     Creates a dictionary with the following structure:
#     {"news tweet id" : [reply_id_1, reply_id_2, ... , reply_id_n]}
#     """
#     f = open(clean_path)
#     data = json.load(f)
#     tweets_list = data["tweets"]

#     news_tweets_dict = {} 
#     for tweet in tweets_list:
#         tweet_id = str(tweet["id"])
#         news_tweets_dict[tweet_id] = [] 
    
#     return news_tweets_dict

def get_reply_ids_list(news_tweet_id):
    """
    Gets a list of reply IDS given a news tweet id.  
    """

    base_command = 'snscrape twitter-tweet --scroll '
    final_command = base_command + news_tweet_id  
    print(final_command) 
    proc = subprocess.run(final_command, capture_output = True)
    reply_ids_list = get_reply_ids(proc.stdout) 
    
    return reply_ids_list   

def get_reply_ids(stdout):
    """
    Takes in the standard output (the list of reply urls). Returns a list of reply ids. 
    """

    reply_urls = stdout.decode()
    # Creates a list of reply urls 
    reply_urls = reply_urls.split('\n')
    reply_ids = [] 

    for url in reply_urls: 
        tweet_id = get_reply_id(url)
        tweet_id = tweet_id.rstrip('\r')
        reply_ids.append(tweet_id) 

    #  Remove the first and last element (dummy elements) 
    if len(reply_ids) > 2:
        reply_ids.pop(0)
        reply_ids.pop() 

    return reply_ids 

def get_reply_id(reply_url):
    """
    Given the reply url, gets the tweet id. 
    """
    tweet_id = ""
    for c in reversed(reply_url):
        if c == "/":
            return tweet_id 
        else:
            tweet_id = c + tweet_id 
    
    return tweet_id    

def parse_response(root_id, response):
    """
    Parse the response dictionary that the Twitter API returns. Get only shallow replies (i.e. replies that are direct to the news tweet itself). 
    """ 

    response_dict = response["data"][0]
    conversation_id = response_dict["conversation_id"]
    
    # Drop the response if it's not a shallow tweet. 
    if conversation_id != root_id: 
        return None 
    else: 
        reply_id = response_dict['id']
        conversation_id = response_dict['conversation_id']
        author_id = response_dict['author_id']
        text = response_dict['text']
        lang = response_dict['lang']
        retweet_count = response_dict['public_metrics']['retweet_count']
        reply_count = response_dict['public_metrics']['reply_count']
        like_count = response_dict['public_metrics']['like_count']
        quote_count = response_dict['public_metrics']['quote_count']

        parsed_response = {"id" : reply_id, "conversation_id" : conversation_id, "author_id" : author_id, "text" : text, "lang" : lang, "retweet_count" : retweet_count, "reply_count" : reply_count, "like_count" : like_count, "quote_count" : quote_count}
        
        return parsed_response 

def main():

    path = "./data_clean/fox_tweets_2020_clean.json"
    f = open(path)
    data = json.load(f)
    tweets_list = data["tweets"]

    # For each reply, get the data. 
    out_file = open("./data_clean/sample.json", "w") 
    resume = False 
    for tweet_dict in tweets_list:
        news_tweet_id = str(tweet_dict["id"])
     
        reply_ids_list = get_reply_ids_list(news_tweet_id)
        print(reply_ids_list) 
        for reply_id in reply_ids_list: 
            url = create_url(reply_id)
            json_response = connect_to_endpoint(url)
            parsed_response = parse_response(news_tweet_id, json_response)  
            if parsed_response == None: 
                continue 
            print(parsed_response) 
            json.dump(parsed_response, out_file) 
            out_file.write('\n')
            time.sleep(3) 

    out_file.close() 




if __name__ == "__main__":
    main() 
    

     
