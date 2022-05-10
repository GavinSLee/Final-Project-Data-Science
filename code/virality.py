from numpy import average
from hypothesis import *
from preprocess import terms


def getAverageViralityPerKeyword():
    cnn_tweets_read_path = "../data_clean/cnn_tweets_clean.json"
    fox_tweets_read_path = "../data_clean/fox_tweets_clean.json"
    out_path = "../data_hypotheses/keyword_average_virality.json"
    all_tweets = load_json(cnn_tweets_read_path) + \
        load_json(fox_tweets_read_path)
    result = {}
    for keyword in terms:
        scores = []
        for tweet in all_tweets:
            if keyword in tweet["keywords"]:
                scores.append(tweet_virality(tweet))
        if len(scores) == 0:
            result[keyword] = 0
        else:
            avg = sum(scores) / len(scores)
            result[keyword] = avg
    save_json(out_path, result)


def main():
    getAverageViralityPerKeyword()


if __name__ == "__main__":
    main()
