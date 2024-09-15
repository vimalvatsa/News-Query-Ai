from DocAssess.Prompts import question_template, question_prompt, category_list
from VectorDB.VectorDB import vector_db
from Query.Utilities import create_search_expresion
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from LLM.Providers import my_llm
from Constants.constants import TypeOfSearch


def assess_doc(header, collection_name, doc_id):

    llm = my_llm(header)

    retriever = vector_db.initialize_db(collection_name, header=header).as_retriever(
        search_type="similarity",
        search_kwargs={"expr": create_search_expresion(doc_id, TypeOfSearch.default)},
    )

    response_dict = {}

    basic_prompt = PromptTemplate(
        template=question_prompt, input_variables=["context", "question"]
    )

    chain_type_kwargs = {"prompt": basic_prompt}

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type_kwargs=chain_type_kwargs,
    )
    index = 0
    for question in question_template:
        category = category_list[index]
        llm_response = qa_chain(question)
        response_dict[category] = llm_response["result"]
        index += 1
    return response_dict
