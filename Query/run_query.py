import html
from langchain.chains import RetrievalQA
from LLM.Providers import my_llm
from VectorDB.VectorDB import vector_db
from Prompts.prompts import Prompts
from Constants.constants import TypeOfSearch
from Query.Utilities import create_search_expression


# def answer_docs(query, searching_doc_id, collection_name, header, type_of_search):
#     retriever = vector_db.initialize_db(collection_name, header).as_retriever(
#         search_type="similarity",
#         search_kwargs={
#             "expr": create_search_expresion(searching_doc_id, type_of_search)
#         },
#     )
#     if type_of_search == TypeOfSearch.default:
#         chain_type_kwargs = {"prompt": Prompts.basic_prompt}
#     elif type_of_search == TypeOfSearch.vault_model:
#         chain_type_kwargs = {"prompt": Prompts.model_prompt}

#     llm = my_llm(header)

#     qa_chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff",
#         retriever=retriever,
#         return_source_documents=True,
#         chain_type_kwargs=chain_type_kwargs,
#     )

#     llm_response = qa_chain(query)

#     result = None

#     source_docs = llm_response["source_documents"]
#     result = llm_response["result"]
#     escaped_text = html.escape(result)
#     html_with_line_breaks = escaped_text.replace("\n", "<br>")

#     result_content = []
#     for docs in source_docs:
#         temp = {}
#         temp["filename"] = docs.metadata.get("filename")
#         temp["page number"] = docs.metadata.get("page_number")
#         page_content = docs.page_content
#         last_full_stop_index = page_content.rfind(".")
#         if last_full_stop_index != -1:
#             temp["text"] = page_content[: last_full_stop_index + 1]
        
#         else:
#             temp["text"] = page_content
#         result_content.append(temp)

#     sorry_query_words = ["Sorry!", "could", "not", "find", "answer", "given", "data"]
#     for words in sorry_query_words:
#         if words in result:
#             citation = False
#         else:
#             citation = True

#     if result is not None:
#         return (html_with_line_breaks, result_content, citation)
#     else:
#         message = "Error! Add documents first."
#         return message


def answer_docs(query, collection_name, header, type_of_search):
    #Create search expression using the function from Utilities.py
    search_expr = create_search_expression(type_of_search, query)
    
    retriever = vector_db.initialize_db(collection_name, header).as_retriever(
        search_type="similarity",
        search_kwargs={
            "expr" : search_expr
        },
    )
    
    if type_of_search == TypeOfSearch.default:
        chain_type_kwargs = {"prompt": Prompts.basic_prompt}
    elif type_of_search == TypeOfSearch.vault_model:
        chain_type_kwargs = {"prompt": Prompts.model_prompt}

    llm = my_llm(header)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs=chain_type_kwargs,
    )

    llm_response = qa_chain(query)

    result = None
    source_docs = llm_response["source_documents"]
    result = llm_response["result"]
    escaped_text = html.escape(result)
    html_with_line_breaks = escaped_text.replace("\n", "<br>")

    result_content = []
    for docs in source_docs:
        temp = {}
        temp["filename"] = docs.metadata.get("filename")
        temp["page number"] = docs.metadata.get("page_number")
        page_content = docs.page_content
        last_full_stop_index = page_content.rfind(".")
        if last_full_stop_index != -1:
            temp["text"] = page_content[: last_full_stop_index + 1]
        else:
            temp["text"] = page_content
        result_content.append(temp)
    sorry_query_words = ["Sorry!", "could", "not", "find", "answer", "given", "data"]
    
    # Check for citation based on result content
    citation = any(word in result for word in sorry_query_words)

    if result is not None:
        return (html_with_line_breaks, result_content, citation)
    else:
        message = "Error! No news articles found."
        return message
 
    