# Factory pattern
from modules.reddit_api import RedditApi
from modules.arxiv_api import ArxivApi
from utils.tools import singleton

# @singleton
class DocumentFactory:
    """
    Factory class for creating documents based on the type of process.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize the DocumentFactory object.
        
        Parameters:
            kwargs (dict): Keyword arguments containing the data for creating the document.
        """
        if kwargs['data']:
            self.data = kwargs['data']
            self.type_process = self.data['type_process']
        else:
            raise ValueError('No data provided')
        
        # self.create_document()
        
    
    def create_document(self):
        """
        Create a document based on the type of process.
        
        Returns:
            object: The created document object.
        """
        if self.type_process.lower() == 'reddit':
            obj = RedditApi(
                self.data['keyword'])
            return obj
        if self.type_process.lower() == 'arxiv':
            return ArxivApi(
                keyword=self.data['keyword'], 
                max_results=self.data['max_results'])
        return None