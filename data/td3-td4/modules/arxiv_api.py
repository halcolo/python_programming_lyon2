import xmltodict
import datetime
import requests
from modules.Document import Document
from tools.progress_bar import print_progress_bar


class ArxivApi:
    def __init__(self, keyword: str, start=0, max_results=1):
        """
        Initializes an instance of the ArxivApi class.
        
        Parameters:
            keyword (str): The keyword to search for in the ArXiv API.
            start (int): The starting index of the search results (default is 0).
            max_results (int): The maximum number of results to retrieve (default is 1).
        """
        self.keyword = keyword
        self.start = start
        self.max_results = max_results
        self.create_query_string(keyword=self.keyword,
                                start=self.start,
                                max_results=self.max_results)

        self.url = None
        self.data = None
        
        self.base_url = 'http://export.arxiv.org/api/query'


    def get_data(self) -> dict | None:
        """
        Retrieves the data from the ArXiv API.
        
        Returns:
            dict | None: The parsed data from the API response, or None if the request failed.
        """
        response = requests.get(url=self.base_url,
                                params=self.query_params)
        if response.status_code == 200:
            self.data = xmltodict.parse(response.content.decode())['feed']
            return self.data['entry']
        else:
            return None
    
    def set_documents(self) -> list:
        """
        Sets the documents based on the retrieved data.
        
        Returns:
            list: A list of Document objects.
        """
        collection = list()
        if self.data is None:
            self.get_data()

        entries = self.data['entry']
        progress = 0
        total = len(entries)
        for document in entries:
            print_progress_bar(progress, total, 'Arxiv process')
            authors = [auth['name'] if isinstance(auth, dict) else auth for auth in document['author']]
            doc = Document(title=document['title'],
                            date=datetime.datetime.strptime(document['published'], 
                                                            "%Y-%m-%dT%H:%M:%SZ").date(),
                            author=authors,
                            url=document['id'],
                            text=str(document['summary']).replace('\n',' ')
            )
            collection.append(doc)
            progress += 1
        return collection
    
    def create_query_string(self, **kwargs):
        """
        Creates the query string for the ArXiv API request.
        
        Parameters:
            **kwargs: The keyword arguments to update the query parameters.
        """
        if 'keyword' in kwargs:
            self.keyword = kwargs['keyword']
        if 'start' in kwargs:
            self.start = kwargs['start']
        if 'max_results' in kwargs:
            self.start = kwargs['max_results']
            
        self.query_params = {
            'search_query': f'all:{self.keyword}',
            'start': self.start,
            'max_results': self.max_results
            }
    