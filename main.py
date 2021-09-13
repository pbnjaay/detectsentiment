from flask_cors import CORS
from flask import Flask
from utils import average
from comprehend import analyse_all_sentiment
from twitter import get_all_replies, get_all_tweets
from scraping import scrap_comment

app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/v1/<user>")
@app.route("/api/v1/<user>/<hashtag>")
def hello_world(user, hashtag=""):
    return analyse_all_sentiment(get_all_tweets(user, hashtag))


@app.route("/api/v1/replies/<conversation_id>/avg")
def avg(conversation_id):
    response = analyse_all_sentiment(get_all_replies(conversation_id))
    return {"average": average(response)}


@app.route("/api/v1/replies/<conversation_id>")
def all_replies(conversation_id):
    response = analyse_all_sentiment(get_all_replies(conversation_id))
    return response


@app.route("/api/v1/seneweb/<type>/<url>")
def get_comment(type, url):
    return analyse_all_sentiment(scrap_comment(type, url))


@app.route("/api/v1/seneweb/<type>/<url>/avg")
def sen_avg(type, url):
    response = analyse_all_sentiment(scrap_comment(type, url))
    return {"average": average(response)}
