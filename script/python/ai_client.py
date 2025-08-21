from openai import OpenAI
from dotenv import load_dotenv
import base64
import os

load_dotenv()

URL = os.environ.get("URL")
API_KEY = os.environ.get("API_KEY")

client = OpenAI(base_url=URL, api_key=API_KEY)


def chat(model: str):
    print(f"Model 名稱: {model}")
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
    print(response.choices[0].message.content)


def edit_image(model: str, prompt: str, input_path: str):
    print(f"Model 名稱: {model}")
    response = client.images.edit(
        model=model,
        image=open(f"test-data/{input_path}", "rb"),
        prompt=prompt,
    )
    result = response.data[0].b64_json
    result = base64.b64decode(result)
    with open(f"test-data/edited-{input_path}", "wb") as f:
        f.write(result)


def parse_image(model: str, image_path: str, text: str):
    print(f"Model 名稱: {model}")
    with open(image_path, "rb") as f:
        image = f.read()
        response = client.responses.create(
            model=model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": text},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/png;base64,{base64.b64encode(image).decode()}",
                        },
                    ],
                },
            ],
        )
        print(response.choices[0].message.content)


# chat("deepseek-default")
# chat("bedrock/us.anthropic.claude-opus-4-20250514-v1:0")
# edit_image("azure/gpt-image-1", "請讓她變可愛一點", "witch-full.png")
# parse_image("azure/gpt-4_1", "blue-red-black.png", "請問這是什麼")
