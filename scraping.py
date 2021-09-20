from bs4 import BeautifulSoup
import requests


def scrap_comment(type, url):
    res_json = {
        'data': [],
        'meta': {'result_count': 0}
    }
    html_doc = requests.get(f"https://www.seneweb.com/news/{type}/{url}").text
    soup = BeautifulSoup(html_doc, 'lxml')
    comments = soup.find_all('div', class_='comment_item_content')
    for index, comment in enumerate(comments):
        res_json["data"].append({"id": index, "text": comment.find('span', recursive=False).text})
        res_json["meta"]["result_count"] += 1

    return res_json
