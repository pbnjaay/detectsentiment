def average(response):
    av = {"MIXED": 0, "NEGATIVE": 0, "NEUTRAL": 0, "POSITIVE": 0}
    for x in response["data"]:
        av[x["sentiment"]] = av[x["sentiment"]]+1

    for k, v in av.items():
        av[k] = v / response["count"]

    return av


def detect_emoji(sens):
    switcher = {
        "MIXED": "😵",
        "NEGATIVE": "😡",
        "NEUTRAL": "😐",
        "POSITIVE": "😀",
    }
    return switcher.get(sens)
