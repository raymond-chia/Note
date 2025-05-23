from openai import OpenAI

URL = ""
API_KEY = ""
MODEL = ""

client = OpenAI(base_url=URL, api_key=API_KEY)
response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "Talk like a wizard. 請使用繁體中文"},
        {
            "role": "user",
            "content": "Who are you?",
        },
    ],
)
print(response.choices[0].message.content)
