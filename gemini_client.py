import os
from google import genai


def get_gemini_client():

    api_key = os.getenv("GEMINI_API_KEY")

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable missing")

    client = genai.Client(api_key=api_key)

    return client, model