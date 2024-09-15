from Constants.constants import TypeOfSearch


def create_metadata(doc_s3_key, doc_id, documents, type_of_search):
    if type_of_search == TypeOfSearch.default:
        doc_id = int(doc_id)
        for docs in documents:
            if "page_number" not in docs.metadata.keys():
                docs.metadata["page_number"] = 1
            docs.metadata = {
                "source": docs.metadata["source"],
                "filename": docs.metadata["filename"],
                "page_number": docs.metadata["page_number"],
                "s3_key": doc_s3_key,
                "document_id": doc_id,
            }
    elif type_of_search == TypeOfSearch.vault_model:
        for docs in documents:
            docs.metadata = {
                "source": docs.metadata["source"],
                "s3_key": doc_s3_key,
                "unique_id": doc_id,
            }
    return documents
