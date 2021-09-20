import requests
import yaml


def create_twitter_url(user: str, hashtag: str):
    max_results = 10
    mrf = "max_results={}".format(max_results)
    q = ""
    if(hashtag == ""):
        q = f"query={hashtag} from:{user}"
    else:
        q = "query={} from:{}".format("%23"+hashtag, user)
    url = f"https://api.twitter.com/2/tweets/search/recent?{mrf}&{q}"
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
