import os
from openai import OpenAI

def get_client() -> OpenAI:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set in your environment.")
    return OpenAI(api_key=key)
