from dataclasses import dataclass
from newsapi import NewsApiClient
from dotenv import load_dotenv
import os
import json


load_dotenv()


# Init
newsapi = NewsApiClient(os.getenv("NEWS_KEY"))


@dataclass
class NewsAPIArticle:
    source: str
    author: str
    title: str
    description: str
    url: str
    url_to_image: str
    published_at: str
    content: str


@dataclass
class NewsAPIResults:
    status: str
    total_results: int
    articles: list[NewsAPIArticle]


def get_headlines(save_to_file=False):
    top_headlines = newsapi.get_top_headlines(
        language="en",
        country="us",
        page_size=20
    )

    if save_to_file:
        path_to_file = os.path.join("outputs", "news.json")
        with open(path_to_file, "w", encoding="utf-8") as f:
            json.dump(top_headlines, f, ensure_ascii=False, indent=2)

    def default(object, d):
        return object if object is not None else d

    # Convert raw API response to our data classes
    articles = []
    for article in top_headlines["articles"]:
        news_article = NewsAPIArticle(
            source=default(
                article["source"]["name"] if article.get("source") else None, None
            ),
            author=default(article.get("author"), None),
            title=default(article.get("title"), None),
            description=default(article.get("description"), None),
            url=default(article.get("url"), None),
            url_to_image=default(article.get("urlToImage"), None),
            published_at=default(article.get("publishedAt"), None),
            content=default(article.get("content"), None),
        )
        articles.append(news_article)

    # Create the results object
    top_headlines = NewsAPIResults(
        status=top_headlines["status"],
        total_results=top_headlines["totalResults"],
        articles=articles,
    )

    return top_headlines


if __name__ == "__main__":
    headlines = get_headlines(save_to_file=True)
    print(f"Status: {headlines.status}")
    print(f"Total Results: {headlines.total_results}")
    for article in headlines.articles:
        print("-" * 3)
        print(f"Title: {article.title}")
        print(f"Description: {article.description}")
        print(f"URL: {article.url}")
        print(f"Published At: {article.published_at}")