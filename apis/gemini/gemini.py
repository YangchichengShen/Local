from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("GEMINI_KEY")

client = genai.Client(api_key=key)

def call_gemini_2_flash(prompt, temperature=0.5):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        # Output a list of the users interests
        contents=prompt,
        config={"temperature": 0.0},
    )
    return response.text

# # Test the function with a sample prompt
# print(call_gemini_2_flash("You are a news aggregator. Provide a summary of the latest news in technology."))