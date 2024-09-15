class Utilities:
    s3_bucket_name = "doc-analyser"
    milvus_host = "127.0.0.1"
    milvus_port = "19530"
    milvus_username = "root"
    milvus_password = "Milvus"


def create_s3_key(collection_name, type_of_search, document_name, document_id):
    s3_key = f"{collection_name}/{type_of_search}/{document_id}_{document_name}"
    return s3_key


def flatten_serializer_errors(errors):
    """
    It return flatten serialzer errors
    """
    error_messages = {}
    for field_name, field_errors in errors.items():
        if isinstance(field_errors, dict):
            for index, field_error in field_errors.items():
                error_messages[field_name] = field_errors[index]
        else:
            error_messages[field_name] = field_errors
    res = ""
    for field_name, field_errors in error_messages.items():
        for field_error in field_errors:
            res += f", {field_error}"
    return res[2:]


allowed_demo_headers = ["vault-uat", "vault-qa", "vault-preprod"]
allowed_citations_headers = ["vault-qa"]


class TypeOfSearch:
    default = "Document"
    vault_model = "Model"
    

