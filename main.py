import requests
import yaml
import boto3
import json

comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')


def create_twitter_url():
    handle = "Macky_Sall"
    hashtag = ""
    max_results = 100
    mrf = "max_results={}".format(max_results)
    q = "query={} from:{}".format(hashtag, handle)
    url = "https://api.twitter.com/2/tweets/search/recent?{}&{}".format(
        mrf, q
    )
    return url


def process_yaml():
    with open("config.yaml") as file:
        return yaml.safe_load(file)


def create_bearer_token(data):
    return data["search_tweets_api"]["bearer_token"]


def twitter_auth_and_connect(bearer_token, url):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    response = requests.request("GET", url, headers=headers)
    return response.json()


def detect_dominant_language(text):
    return comprehend.detect_dominant_language(Text=text)


def analyse_sentiment(text, language_code):
    print('Calling DetectSentiment')
    print(text)
    print(json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode=language_code), sort_keys=True, indent=4))
    print('End of DetectSentiment\n')


def main():
    url = create_twitter_url()
    data = process_yaml()
    bearer_token = create_bearer_token(data)
    res_json = twitter_auth_and_connect(bearer_token, url)
    for x in res_json["data"]:
        lang = detect_dominant_language(x["text"])
        analyse_sentiment(x["text"], lang["Languages"][0]["LanguageCode"])


if __name__ == "__main__":
    main()
