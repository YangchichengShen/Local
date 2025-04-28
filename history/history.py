# pip install browser-history dotenv google-genai

import os
import re
from collections import Counter

from browser_history import get_history
from dotenv import load_dotenv
from google import genai
from browser_history.browsers import Chrome

# if windows, set to False. if mac, set to True.
using_windows = False

MAX_URL_LENGTH = 100
HISTORY_CACHE_FILE = "history.txt"
HISTORY_CUTOFF = 100000


load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))


def truncate_url(url):
    if url[-1] != "/":
        url += "/"

    return url[: url.rfind("/", 0, MAX_URL_LENGTH)]


if not os.path.isfile(HISTORY_CACHE_FILE):
    if using_windows:
        outputs = get_history()
    else:
        outputs = Chrome().fetch_history()
    raw_history = outputs.histories
    with open(HISTORY_CACHE_FILE, "w", encoding="utf-8") as f:
        for h in raw_history:
            f.write(truncate_url(h[1]) + " " + h[2] + "\n")

history = []
with open(file=HISTORY_CACHE_FILE, mode="r", encoding="utf-8") as f:
    lines = f.readlines()[1:]
    for line in lines:
        history.append(line.strip())
history = history[-HISTORY_CUTOFF:]

history_words = re.split(r"[/ ()\[\],:|]", " ".join(history))
history_words = [word for word in history_words if len(word) > 2 and len(word) < 20]
history_words_counter = Counter(history_words)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Here is word count data of the browser history of a user. Summarize the data in a few words. "
    + str(history_words_counter.most_common(200)),
    config={"temperature": 0.0},
)

print(response.text)
