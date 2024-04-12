from openai import OpenAI
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
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")


def append_data(df, worksheet, number_of_cols):
    values = worksheet.get_all_values()
    col = colnumn_string(max([len(r) for r in values]) + 1)
    worksheet.add_cols(number_of_cols)
    worksheet.update(
        values=df.values.tolist(),
        range_name=col + "2",
        value_input_option="USER_ENTERED",
    )


def colnumn_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 2, 26)
        string = chr(65 + remainder) + string
    return string


def lm_completion(messages: list[dict]) -> str:

    client = OpenAI(api_key=OPENAI_API_KEY)

    logger.info("Messages: %s", messages)
    start = time.perf_counter()
    response = client.chat.completions.create(
        messages=messages, model=OPENAI_MODEL_NAME
    )
    request_time = time.perf_counter() - start
    logger.info("Response Time: %s", request_time)
    logger.info("Response: %s", response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip()
