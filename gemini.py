from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()
key = os.getenv("GEMINI_KEY")

client = genai.Client(api_key=key)


def call_gemini_2_flash(prompt, temperature=0.0, schema=None):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            "temperature": 0.0,
            "response_mime_type": "application/json" if schema is not None else None,
            "response_schema": schema,
        },
    )

    return json.loads(response.text) if schema is not None else response.text
