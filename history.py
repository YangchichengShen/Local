import os
import re
import json
import datetime
from collections import Counter

from browser_history import get_history
from dotenv import load_dotenv
from google import genai
from browser_history.browsers import Chrome

# if windows, set to False. if mac, set to True.
using_windows = False

MAX_URL_LENGTH = 100
OUTPUT_DIR = "outputs"
HISTORY_CACHE_FILE = "history.txt"
HISTORY_CUTOFF = 100000


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_KEY"))


def truncate_url(url):
    if url[-1] != "/":
        url += "/"

    return url[: url.rfind("/", 0, MAX_URL_LENGTH)]


# define output directory to store results
os.makedirs(OUTPUT_DIR, exist_ok=True)

filepath = os.path.join(OUTPUT_DIR, HISTORY_CACHE_FILE)
if not os.path.isfile(filepath):
    if using_windows:
        outputs = get_history()
    else:
        outputs = Chrome().fetch_history()
    raw_history = outputs.histories
    with open(filepath, "w", encoding="utf-8") as f:
        for h in raw_history:
            f.write(truncate_url(h[1]) + " " + h[2] + "\n")

history = []
with open(filepath, mode="r", encoding="utf-8") as f:
    lines = f.readlines()[1:]
    for line in lines:
        history.append(line.strip())
history = history[-HISTORY_CUTOFF:]

history_words = re.split(r"[/ ()\[\],:|]", " ".join(history))
history_words = [word for word in history_words if len(word) > 2 and len(word) < 20]
history_words_counter = Counter(history_words)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    # Output a list of the users interests
    contents=(
        "Given the following word count data extracted from a user's browser history, "
        "analyze it and output ONLY a JSON object listing the user's categories of interests. "
        "Respond ONLY with valid JSON and nothing else. The schema should be:\n\n"
        "{\n"
        '  "interests": ["string", "string", ...]\n'
        "}\n\n"
        "Here is the word count data: " + str(history_words_counter.most_common(200))
    ),
    config={"temperature": 0.0},
)

# view what Gemini actually said
# print("Raw Gemini output:\n", response.text)

raw_text = response.text.strip()

# check that Gemini responded with something
if not raw_text:
    raise ValueError("Empty Gemini Response")

# use regex to extract content inside backticks
if raw_text.startswith("```"):
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
    if match:
        json_text = match.group(1)
        print(json_text)
    else:
        raise ValueError("Could not find valid JSON inside triple backticks.")
else:
    json_text = raw_text

# parse gemini output text to json
try:
    interests = json.loads(json_text)
except json.JSONDecodeError as e:
    raise ValueError(f"Failed to parse Gemini output as JSON: {e}")

# print output
print("Interests parsed:\n", interests["interests"])

# define filename and file path
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = "interests.json"
filepath = os.path.join(OUTPUT_DIR, filename)

# save json
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(interests, f, indent=2)

print(f"Output saved to {filepath}")
