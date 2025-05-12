from gemini import call_gemini_2_flash
import json
import os

news_json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "news", "news.json")

with open(news_json_path, "r", encoding="utf-8") as f:
    example_news = json.load(f)['articles']

interests_json = {
  "interests": [
    "Patents",
    "Product Design",
    "Furniture Design (Desks, Chairs)",
    "Education (Courses, Lectures, Assignments)",
    "Job Search/Career Opportunities",
    "Fashion (Aritzia)",
    "Computer Science",
    "Security",
    "University Life (Northwestern)",
    "Online Collaboration Tools (Google Docs, Slides, Notion)",
    "Social Media (LinkedIn, Instagram)",
    "Research",
    "Internships"
  ]
}

contextify_prompt = '''
You are a news aggregator. Given the following interests, provide a contextified summary of the latest news that would be relevant to these interests. Respond with a JSON object where each key is an interest and the value is a brief news blurb related to that interest (at least 3 sentences). The schema should be:

{
  "interest1": "news blurb for interest1",
  "interest2": "news blurb for interest2",
  ...
}
You do not include all interests in the output, only the ones that have relevant news.
'''

# TODO: Change the interests_json and example_news to be dynamic based on user input or session state
def get_contextified_news(interests=interests_json, news=example_news):
    # Call the Gemini API to get the news contextified to the interests
    prompt = contextify_prompt + "\n\n" + str(interests) + "\n\n" + str(news)
    result = call_gemini_2_flash(
        prompt = prompt,
        temperature=0.0
    )
    return result

# print(get_contextified_news(interests_json, example_news))
