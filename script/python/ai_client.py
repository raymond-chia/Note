from openai import OpenAI
from dotenv import load_dotenv
import base64
import os

load_dotenv()

URL = os.environ.get("URL")
API_KEY = os.environ.get("API_KEY")

client = OpenAI(base_url=URL, api_key=API_KEY)


def chat(model: str):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "請使用繁體中文"},
            {
                "role": "user",
                "content": "你好",
            },
        ],
    )
    print(f"Model 名稱: {model}")
    print(response.choices[0].message.content)


def edit_image(model: str, prompt: str, input_path: str):
    response = client.images.edit(
        model=model,
        image=open(f"test-data/{input_path}", "rb"),
        prompt=prompt,
    )
    result = response.data[0].b64_json
    result = base64.b64decode(result)
    with open(f"test-data/edited-{input_path}", "wb") as f:
        f.write(result)


# chat("gpt-default")
# chat("bedrock/us.anthropic.claude-opus-4-20250514-v1:0")
edit_image("azure/gpt-image-1", "請讓她變可愛一點", "witch-full.png")
