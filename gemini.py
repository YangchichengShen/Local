from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("GEMINI_KEY")

client = genai.Client(api_key=key)


def call_gemini_2_flash(prompt, temperature=0.0):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        # Output a list of the users interests
        contents=prompt,
        config={"temperature": temperature},
    )
    return response.text
