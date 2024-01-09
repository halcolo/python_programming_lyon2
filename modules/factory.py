# Factory pattern
from modules.api import RedditApi
from modules.api import ArxivApi
    
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
        self.validate_data(kwargs)
        self.data = kwargs['data']
        self.type_process = self.data['type_process']

    def validate_data(self, kwargs):
        """
        Validate the input data.

        Parameters:
            kwargs (dict): The input data.
        """
        if 'data' not in kwargs or not kwargs['data']:
            raise ValueError('No data provided')

    def create_document(self):
        """
        Create a document based on the type of process.

        Returns:
            object: The created document object.
        """
        type_to_class = {
            'reddit': RedditApi,
            'arxiv': ArxivApi
        }

        if self.type_process.lower() not in type_to_class:
            raise ValueError(f'Unsupported type: {self.type_process}')

        if self.type_process.lower() == 'reddit':
            return type_to_class[self.type_process.lower()](
                self.data['keyword'])
        if self.type_process.lower() == 'arxiv':
            return type_to_class[self.type_process.lower()](
                keyword=self.data['keyword'],
                max_results=self.data['max_results'])