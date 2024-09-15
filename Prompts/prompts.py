from langchain.prompts import PromptTemplate
from Prompts.basic import basic_template
from Prompts.vault_model import model_template


class Prompts:
    basic_prompt = PromptTemplate(
        template=basic_template, input_variables=["context", "question", "news_article"]
    )
    model_prompt = PromptTemplate(
        template=model_template, input_variables=["context", "question", "news_article"]
    )
