import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

load_dotenv()
key = os.getenv("GEMINI_KEY")

genai.configure(api_key=key)

def call_gemini_2_flash(prompt, temperature=0.0, schema=None):
    model = genai.GenerativeModel("gemini-2.0-flash")

    response = model.generate_content(
        contents=prompt,
        generation_config={
            "temperature": temperature,
        }
    )

    return json.loads(response.text) if schema is not None else response.text