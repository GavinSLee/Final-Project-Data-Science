import json 
from transformers import pipeline 
from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoConfig

########################## Assigns Sentiment Scores ##########################


def load_classifier(model_name): 
    """
    Loads the sentiment classifier that we are using via HuggingFace and Transformers. 
    """

    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    config = AutoConfig.from_pretrained(model_name)
    classifier = pipeline("sentiment-analysis", model = model, tokenizer = tokenizer, config = config)
    return classifier 

def assign_sentiment(classifier, reply):
    """
    Assigns a sentiment number to the reply dictionary passed into the function.
    """

    reply.pop('sentiment', None)
    tweet_text = [reply["text"]]
    sentiment = classifier(tweet_text)[0]
    reply["sentiment_label"] = sentiment['label'] 
    reply["sentiment_score"] = sentiment['score']

    print(sentiment) 
    return reply 

def get_data_with_sentiment(classifier, read_path, write_path):
    """
    Adds the individual sentiment scores to each reply dictionary in the list and overwrites the file.
    """

    with open(read_path, 'r') as f:
        reply_list = json.load(f)

    for i in range(20518, len(reply_list)):
        print("Current Iteration: " + str(i) + " out of " + str(len(reply_list))) 
        reply = reply_list[i] 
        assign_sentiment(classifier, reply) 

        with open(write_path, 'r+') as f:
            new_replies = json.load(f) 
            new_replies.append(reply) 
            f.seek(0) 
            json.dump(new_replies, f) 


########################## Handles Cross Validation ##########################





########################## Main Function ##########################


def main():
    model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    classifier = load_classifier(model_name) 

    cnn_replies_read_path = "../data_clean/cnn_replies_clean.json"
    cnn_replies_write_path = "../data_clean/cnn_replies_clean_sentiment.json"
    # fox_replies_read_path = "../data_clean/fox_replies_clean.json"
    # fox_replies_write_path = "../data_clean/fox_replies_clean_sentiment.json"

    get_data_with_sentiment(classifier, cnn_replies_read_path, cnn_replies_write_path)
    # get_data_with_sentiment(classifier, fox_replies_read_path, fox_replies_write_path) 
        
if __name__ == "__main__":
    main() 




