from Constants.constants import TypeOfSearch
# import nltk
# nltk.download('punkt')

def create_collection_name(header, type_of_search, user_id=None):
    """Makes collection name on the basis of header and search type"""
    header = header.replace("-", "_")
    collection_name = header + "_" + type_of_search + "_" + user_id if user_id else header + "_" + type_of_search
    return collection_name


def create_response(type_of_search, document_id):
    if type_of_search == TypeOfSearch.default:
        response = {
            "message": "Document uploaded successfully",
            "documentID": document_id,
        }
    elif type_of_search == TypeOfSearch.vault_model:
        response = {
            "message": "Model uploaded successfully",
            "modelID": document_id,
            "status": True,
        }
    return response

def result_file_response(document_id, chat_id, file_name):
    response = {
        "message": "File uploaded successfully",
        "documentID": document_id,
        "chatID": chat_id,
        "fileName": file_name,
    }
    return response
