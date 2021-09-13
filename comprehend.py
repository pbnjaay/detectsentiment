from utils import detect_emoji
import boto3


comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')


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


def detect_dominant_language(text):
    return comprehend.detect_dominant_language(Text=text)
