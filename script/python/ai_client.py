from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

URL = os.environ.get("URL")
API_KEY = os.environ.get("API_KEY")
MODEL = os.environ.get("MODEL")

client = OpenAI(base_url=URL, api_key=API_KEY)
response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "請使用繁體中文"},
        {
            "role": "user",
            "content": "你好",
        },
    ],
)
print(f"Model 名稱: {MODEL}")
print(response.choices[0].message.content)
