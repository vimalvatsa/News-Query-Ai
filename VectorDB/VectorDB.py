"""Vector DB Managaer File. All vector operations of platform should call this class object"""
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from Application.models import ChatBox
from VectorDB.Providers.Milvus import milvus_db

provider_map = {"Milvus": milvus_db}
current_provider = "Milvus"


class VectorDbManager:
    """Vector DB Class"""

    def __init__(self):
        self.provider = provider_map[current_provider]

    def add_files(self, doc_s3_key, doc_id, collection_name, header, type_of_search):
        return self.provider.add_files(doc_s3_key, doc_id, collection_name, header, type_of_search)

    def delete_files(self, doc_id, collection_name, type_of_search):
        return self.provider.delete_files(doc_id, collection_name, type_of_search)

    def check_file_existence(self, doc_id, collection_name, type_of_search):
        return self.provider.check_file_existence(doc_id, collection_name, type_of_search)

    def initialize_db(self, collection_name, header):
        return self.provider.initialize_db(collection_name, header)
    
    
    def check_article_exists(self, documentName, dock_key, content):
        collection_name = "news_articles"
        return self.provider.check_news_article_exists(collection_name, documentName, dock_key)
    
    def add_document(self,documentName, doc_key, content):
        """
        Add a document to the vector database.
        
        :param doc_id: The ID of the document
        :param doc_key: The key or URL of the document
        :param content: The content of the document to be vectorized
        :return: True if successful, False otherwise
        """
        try:
            collection_name = "news_articles"
            
            if not self.provider.check_collection_exist(collection_name):
                self.provider.initialize_db(collection_name, "news")
            
            #vectorising the content
            vector = self.provider.vectorize_text(content)
            
            self.provider.insert_vectors(collection_name, [documentName], [vector],[{"doc_key": doc_key, "content": content}])
            
            return True
        except Exception as e:
            print(f"An error occurred while adding document to vector database: {e}")
            return False
            
    def get_article_data(self, documentName):
        """Retrieve article data from the vector database"""
        collection_name = "news_articles"
        return self.provider.get_news_article_data(collection_name, documentName)
    
    # def __init__(self):
    #     self.provider = provider_map[current_provider]
    #     self.engine = create_engine('your_database_url')
    #     Session = sessionmaker(bind=self.engine)
    #     self.session = Session()

    def get_chat_data(self, chat_id):
        """Retrieve chat data based on chat_id."""
        try:
            stmt = select(ChatBox).where(ChatBox.resultID == chat_id)
            result = self.session.execute(stmt).fetchone()
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

vector_db = VectorDbManager()


