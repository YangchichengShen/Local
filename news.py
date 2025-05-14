from newsapi import NewsApiClient
import json
from dotenv import load_dotenv
import os


load_dotenv()


# Init
newsapi = NewsApiClient(os.getenv("NEWS_KEY"))

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(
    language="en",
    country="us",
)

json_formatted_str = json.dumps(top_headlines, indent=2)

print(json_formatted_str)

path_to_file = os.path.join("outputs", "news.json")
with open(path_to_file, "w", encoding="utf-8") as f:
    json.dump(top_headlines, f, ensure_ascii=False, indent=2)
