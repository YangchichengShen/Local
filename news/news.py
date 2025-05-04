# See https://newsapi.org/
# pip install newsapi-python

from newsapi import NewsApiClient
import json
from dotenv import load_dotenv
import os


load_dotenv()


# Init
newsapi = NewsApiClient(os.getenv("NEWSAPI_KEY"))

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(
    language="en",
    country="us",
)

json_formatted_str = json.dumps(top_headlines, indent=2)

print(json_formatted_str)

with open("news.json", "w", encoding="utf-8") as f:
    json.dump(top_headlines, f, ensure_ascii=False, indent=2)
