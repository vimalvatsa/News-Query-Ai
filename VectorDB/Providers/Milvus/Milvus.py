"""Main file of Milvus Vector Database"""
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from VectorDB.Providers.Base import VectorDBProvider
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Milvus
from langchain.document_loaders import S3FileLoader
from pymilvus import connections, Collection
from Constants.constants import Utilities, TypeOfSearch
from Embeddings.Providers import my_embedding
from VectorDB.Providers.Milvus.Utilities import create_metadata


class MilvusDB(VectorDBProvider):
    def __init__(self):
        """No params"""
        pass

    def add_files(self, doc_s3_key, doc_id, collection_name, header, type_of_search):
        loader = S3FileLoader(bucket=Utilities.s3_bucket_name, key=doc_s3_key)
        loader.mode = "paged"
        documents = loader.load()
        documents = create_metadata(doc_s3_key, doc_id, documents, type_of_search)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=0, separators=[" ", ",", "\n"]
        )
        docs = text_splitter.split_documents(documents)

        Milvus.from_documents(
            documents=docs,
            embedding=my_embedding(header),
            connection_args={
                "host": Utilities.milvus_host,
                "port": Utilities.milvus_port,
                "user": Utilities.milvus_username,
                "password": Utilities.milvus_password,
            },
            collection_name=collection_name,
        )

    def delete_files(self, doc_id, collection_name, type_of_search):
        connections.connect(
            host=Utilities.milvus_host,
            port=Utilities.milvus_port,
            user=Utilities.milvus_username,
            password=Utilities.milvus_password,
        )

        collection = Collection(collection_name)
        if type_of_search == TypeOfSearch.default:
            doc_id = int(doc_id)
            res = collection.query(
                expr=f"pk >= 0 && document_id in {[doc_id]}", output_fields=["pk"]
            )
        elif type_of_search == TypeOfSearch.vault_model:
            res = collection.query(
                expr=f"pk >= 0 && unique_id in {[doc_id]}", output_fields=["pk"]
            )
        deleting_doc_pk_list = []
        for x in res:
            deleting_doc_pk_list.append(x["pk"])

        expr = f"pk in {deleting_doc_pk_list}"
        collection.delete(expr)
        deleting_doc_pk_list.clear()

    def check_file_existence(self, doc_id, collection_name, type_of_search):
        connections.connect(
            host=Utilities.milvus_host,
            port=Utilities.milvus_port,
            user=Utilities.milvus_username,
            password=Utilities.milvus_password,
        )
        try:
            collection = Collection(collection_name)
        except Exception:
            return False
        if type_of_search == TypeOfSearch.default:
            doc_id = int(doc_id)
            result = collection.query(
                expr=f"document_id in {[doc_id]}", output_fields=["document_id"]
            )
        elif type_of_search == TypeOfSearch.vault_model:
            result = collection.query(
                expr=f"unique_id in {[doc_id]}", output_fields=["unique_id"]
            )
        if len(result) == 0:
            return False
        else:
            return True

    def initialize_db(self, collection_name, header):
        vector_db = Milvus(
            embedding_function=my_embedding(header),
            connection_args={
                "host": Utilities.milvus_host,
                "port": Utilities.milvus_port,
                "user": Utilities.milvus_username,
                "password": Utilities.milvus_password,
            },
            collection_name=collection_name,
        )
        return vector_db
    
    def check_collection_exist(self, collection_name):
        connections.connect(
            host=Utilities.milvus_host,
            port=Utilities.milvus_port,
            user=Utilities.milvus_username,
            password=Utilities.milvus_password,
        )
        try:
            collection = Collection(collection_name)
        except Exception:
            return False
        return True
    
    def check_news_article_exists(self, collection_name, documentName, doc_key):
        """Check if a news article exists in the vector database"""
        connections.connect(
            host=Utilities.milvus_host,
            port=Utilities.milvus_port,
            user=Utilities.milvus_username,
            password=Utilities.milvus_password,
        )
        try:
            collection = Collection(collection_name)
        except Exception:
            return False
        collection.load()
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        # Query the collection for the document
        result = collection.query(
            data=[self.vectorize_text(documentName)],
            anns_field="embedding",
            param=search_params,
            limit=1,
            expr=f'documentName == "{documentName}"',
            expri=f"doc_key == '{doc_key}'",
            output_fields=["documentName","doc_key", "content"]
        ) 

        return len(result[0]) > 0
    
    def get_news_article_data(self, collection_name, documentName):
        """Retrieve news article data from the collection"""
        collection = Collection(collection_name)
        collection.load()
        
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        results = collection.search(
            data=[self.vectorize_text(documentName)],
            anns_field="embedding",
            param=search_params,
            limit=1,
            expr=f'documentName == "{documentName}"',
            output_fields=["content"]
        )
        
        if len(results[0]) > 0:
            return {"content": results[0][0].entity.get("content")}
        return None
    
    def vectorize_text(self, text, header=None):
        """Vectorize text using the embedding model"""
        embedding_function = my_embedding(header)
        vector = embedding_function.embed_query(text)
        return vector
    
    def insert_vectors(self, collection_name, ids, vectors, metadata):
        """Insert vectors into the collection"""
        if not self.check_collection_exists(collection_name):
            # If collection doesn't exist, create it
            self.create_collection(collection_name)

        collection = Collection(collection_name)
        collection.load()

        entities = [
            ids,
            vectors,
            [m['doc_key'] for m in metadata],
            [m['content'] for m in metadata]
        ]

        try:
            collection.insert(entities)
            collection.flush()
            return True
        except Exception as e:
            print(f"Error inserting vectors: {e}")
            return False

milvus_db = MilvusDB()
