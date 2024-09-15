"""Base class for Vector Storage Provider"""

from abc import ABC, abstractmethod


class VectorDBProvider(ABC):
    """Base class for Vector Storage Provider"""

    def __init__(self):
        """Inherited class will use accordingly"""
        pass

    @abstractmethod
    def add_files(self, **kwargs):
        pass

    @abstractmethod
    def delete_files(self, **kwargs):
        pass

    @abstractmethod
    def check_file_existence(self, **kwargs):
        pass

    @abstractmethod
    def initialize_db(self, **kwargs):
        pass
