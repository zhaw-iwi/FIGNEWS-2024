import openai
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

# setup azureopenai credentials
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_DEPLOYMENT_ENDPOINT = os.getenv("OPENAI_DEPLOYMENT_ENDPOINT")
OPENAI_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")
OPENAI_DEPLOYMENT_VERSION = os.getenv("OPENAI_DEPLOYMENT_VERSION")


def lm_completion(messages: list[dict]) -> str:

    client = AzureOpenAI(
        azure_endpoint=OPENAI_DEPLOYMENT_ENDPOINT,
        api_key=OPENAI_API_KEY,
        api_version=OPENAI_DEPLOYMENT_VERSION,
    )
    response = client.chat.completions.create(
        messages=messages, model=OPENAI_MODEL_NAME
    )
    return response.choices[0].message.content.strip()
