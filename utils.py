from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import logging
import time


# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Create a file handler and set the formatter
file_handler = logging.FileHandler("openai.log", "a", "utf-8")
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

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

    logger.info("Messages: %s", messages)
    start = time.perf_counter()
    response = client.chat.completions.create(
        messages=messages, model=OPENAI_MODEL_NAME
    )
    request_time = time.perf_counter() - start
    logger.info("Response Time: %s", request_time)
    logger.info("Response: %s", response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip()
