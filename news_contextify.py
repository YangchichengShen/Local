from gemini import call_gemini_2_flash
import json
import os

news_json_path = "outputs/news.json"

with open(news_json_path, "r", encoding="utf-8") as f:
    example_news = json.load(f)['articles']

interests_path = "outputs/interests.json"
with open(interests_path, "r", encoding="utf-8") as f:
    interests_json = json.load(f)

'''
contextify_prompt = 
You are a news aggregator. Given the following interests, provide a contextified summary of the latest news that would be relevant to these interests. Respond with a JSON object where each key consistsed of one or more interests and the value is a brief news blurb related to that interest (at least 3 sentences). The schema should be:

{
  "interests": "news blurb for interest1",
  "interests": "news blurb for interest2",
  ...
}
You do not include all interests in the output, only the ones that have relevant news. Each news article should only appear once.
'''

contextify_prompt = '''
You are a news aggregator. Given the following interests and news articles, provide a contextified summary of the latest news that would be relevant to these interests, even if the connection is not obvious or clearly stated in the article. 

Respond with a JSON object where each key is the exact title of ONE news article (copy the title field exactly), and the value is an object with:

{
  "interests": [list of matching interests],
  "summary": "brief news blurb (at least 3 sentences) that explains why this article is relevant to each ofthose interests"
}

Each news article should only appear once, and include articles that are at least slightly relevant to at least one interest.

Here are the interests:
'''

def get_contextified_news(interests=interests_json, news=example_news):
    # Call the Gemini API to get the news contextified to the interests
    prompt = contextify_prompt + "\n\n" + str(interests) + "\n\n" + str(news)
    result = call_gemini_2_flash(
        prompt = prompt,
        temperature=0.0
    )
    return result

# print(get_contextified_news(interests_json, example_news))
