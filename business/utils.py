import google.generativeai as genai
import os
import json
from datetime import datetime
import requests
from functools import lru_cache
from .models import News

genai.configure(api_key="AIzaSyBOW2L_bcv8mEtPBWT0ulVxC8ijUIFkkBk")
model = genai.GenerativeModel("gemini-1.5-flash")
# @lru_cache(maxsize=10)


def get_news_fast():
    """
    Get the news of the day. If news of the day is present in the database,
    then return it. Otherwise, fetch the news from newsapi and then translate
    it using the generative model. Store the data in the database and return it.

    Returns:
    A tuple of english news titles and hindi news titles.
    """
    date_todays = datetime.now().date()
    news = News.objects.filter(created_at=date_todays)
    print(news)
    if news:
        return news[0].english_news, news[0].hindi_news

    news_titles = []
    category = ["business", "general", "health", "science", "sports", "technology"]
    for i in category:
        response = requests.get(
            f"https://saurav.tech/NewsAPI/top-headlines/category/{i}/in.json"
        )
        if response.status_code == 200:
            data = response.json()
            for i in data["articles"][:5]:
                news_titles.append(str(i["title"]))
        else:
            print(f"Error: {response.status_code}")

    response = model.generate_content(
        f"Convert this json to hindi and dont give any other text or anything jsut want hindi converted json string: {json.dumps(news_titles)}"
    )

    News.objects.create(
        english_news=news_titles, hindi_news=list(json.loads(response.text))
    )
    if news:
        news[0].delete()
    return news_titles, json.loads(response.text)
