from openai import OpenAI
from dotenv import load_dotenv
import base64
import os

load_dotenv()


# # Make sure to set up your Google credentials beforehand:
# cp ~/.config/gcloud/application_default_credentials.json gcloud-credential.json
# export GOOGLE_APPLICATION_CREDENTIALS=gcloud-credential.json
def init_gemini_client(
    project_id: str, location: str, impersonated_email: str | None = None
) -> OpenAI:
    from google.auth import default, impersonated_credentials
    import google.auth.transport.requests

    if not project_id or not location:
        raise ValueError(
            "Please set the PROJECT_ID and LOCATION environment variables."
        )

    scopes = ["https://www.googleapis.com/auth/cloud-platform"]

    # https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/openai
    def get_credentials() -> google.auth.credentials.Credentials:
        credentials, _ = default(scopes=scopes)
        credentials.refresh(google.auth.transport.requests.Request())
        return credentials

    def get_impersonated_credentials(
        impersonated_email: str,
    ) -> google.auth.credentials.Credentials:
        source_credentials, _ = default(scopes=scopes)
        impersonated_creds = impersonated_credentials.Credentials(
            source_credentials=source_credentials,
            target_principal=impersonated_email,
            target_scopes=scopes,
            lifetime=3600,  # 短期權杖的有效期限 (秒), 預設 1 小時 (3600)
        )
        impersonated_creds.refresh(google.auth.transport.requests.Request())
        return impersonated_creds

    if impersonated_email:
        credentials = get_impersonated_credentials(impersonated_email)
    else:
        credentials = get_credentials()
    return OpenAI(
        base_url=f"https://aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/openapi",
        api_key=credentials.token,
    )


def init_openai_client(url: str, api_key: str) -> OpenAI:
    return OpenAI(base_url=url, api_key=api_key)


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


load_dotenv()


# client = init_openai_client(
#     os.environ.get("URL", ""),
#     os.environ.get("API_KEY", ""),
# )

# chat("deepseek-default")
# chat("bedrock/us.anthropic.claude-opus-4-20250514-v1:0")
# edit_image("azure/gpt-image-1", "請讓她變可愛一點", "witch-full.png")
# parse_image("azure/gpt-4_1", "blue-red-black.png", "請問這是什麼")


# client = init_gemini_client(
#     os.environ.get("PROJECT_ID", ""),
#     os.environ.get("LOCATION", "global"),
# )
# chat("google/gemini-2.5-flash")
# chat("openai/gpt-oss-120b-maas")
