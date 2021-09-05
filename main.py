import requests
import yaml
import boto3
from flask_cors import CORS
from flask import Flask

app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')


@app.route("/api/v1/<user>")
@app.route("/api/v1/<user>/<hashtag>")
def hello_world(user, hashtag=""):
    return analyse_all_sentiment(get_all_tweets(user, hashtag))


@app.route("/api/v1/replies/<conversation_id>/avg")
def avg(conversation_id):
    response = analyse_all_sentiment(get_all_replies(conversation_id))
    av = {"MIXED": 0, "NEGATIVE": 0, "NEUTRAL": 0, "POSITIVE": 0}
    for x in response["data"]:
        av[x["sentiment"]] = av[x["sentiment"]]+1

    for k, v in av.items():
        av[k] = v / response["count"]
    return {"average": av}


@app.route("/api/v1/replies/<conversation_id>")
def all_replies(conversation_id):
    response = analyse_all_sentiment(get_all_replies(conversation_id))
    return response


def create_twitter_url(user: str, hashtag: str):
    max_results = 10
    mrf = "max_results={}".format(max_results)
    q = ""
    if(hashtag == ""):
        q = "query={} from:{}".format(hashtag, user)
    else:
        q = "query={} from:{}".format("%23"+hashtag, user)
    url = "https://api.twitter.com/2/tweets/search/recent?{}&{}".format(mrf, q)
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


def analyse_sentiment(text, language_code, id):
    response = comprehend.detect_sentiment(Text=text, LanguageCode=language_code)
    return {
        "id": id,
        "text": text,
        "sentiment": response["Sentiment"],
        "score": response["SentimentScore"],
        "language": language_code,
        "emoji": detect_emoji(response["Sentiment"])
    }


def detect_emoji(sens):
    switcher = {
        "MIXED": "😵",
        "NEGATIVE": "😡",
        "NEUTRAL": "🥱",
        "POSITIVE": "😀",
    }
    return switcher.get(sens)


def get_all_tweets(user, hashtag):
    url = create_twitter_url(user, hashtag)
    data = process_yaml()
    bearer_token = create_bearer_token(data)
    res_json = twitter_auth_and_connect(bearer_token, url)
    return res_json


def get_all_replies(conversation_id):
    max_results = 30
    mrf = "max_results={}".format(max_results)
    url = "https://api.twitter.com/2/tweets/search/recent?{}&query=conversation_id:{}".format(mrf, conversation_id)
    data = process_yaml()
    bearer_token = create_bearer_token(data)
    res_json = twitter_auth_and_connect(bearer_token, url)
    return res_json


def analyse_all_sentiment(res_json):
    response = []
    langs = ["ar", "hi", "ko", "zh-TW", "ja", "zh", "de", "pt", "en", "it", "fr", "es"]
    count = res_json["meta"]["result_count"]
    if(count > 0):
        for x in res_json["data"]:
            id = x["id"]
            lang = detect_dominant_language(x["text"])
            dominant = lang["Languages"][0]["LanguageCode"]
            if(dominant in langs):
                response.append(analyse_sentiment(x["text"], dominant, id))
        return {"data": response, "count": count}
    return {"message": "No result 😢"}
