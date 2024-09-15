from DocSearch.settings import config, DEMO_CONFIG, DEFAULT_CONFIG
from langchain.llms import anthropic, OpenAI
from Constants.constants import allowed_demo_headers
import os

os.environ["OPENAI_API_KEY"] = DEMO_CONFIG["api_key"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


def my_llm(header):
    if config["Demo"]:
        openai_llm = OpenAI(
            openai_api_key=OPENAI_API_KEY,
            model="gpt-3.5-turbo-instruct",
            temperature=0.00,
            max_tokens=2000
        )
        return openai_llm
    else:
        anthropic_llm = anthropic.Anthropic(
            anthropic_api_key=DEFAULT_CONFIG["api_key"],
            model_name="claude-2.1",
            max_tokens=2001,
            temperature=0
        )
        return anthropic_llm
