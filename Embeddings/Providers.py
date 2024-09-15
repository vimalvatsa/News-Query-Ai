from langchain.embeddings import HuggingFaceEmbeddings
from langchain.embeddings import OpenAIEmbeddings
from DocSearch.settings import config, DEMO_CONFIG
from Constants.constants import allowed_demo_headers
import os

os.environ["OPENAI_API_KEY"] = DEMO_CONFIG["api_key"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


def my_embedding(header):
    if config["Demo"]:
        openai_embeddings=OpenAIEmbeddings(model='text-embedding-3-small')
        return openai_embeddings
    else:
        hf_embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-l6-v2"
    )
        return hf_embeddings
