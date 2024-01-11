import xmltodict
import datetime
import requests
from modules.document import ArxivDocument
from utils.tools import print_progress_bar


class ArxivApi:
    
    _instance = None
    
    #Singleton pattern
    def __new__(cls, keyword, start=0, max_results=1):
        """
        Initializes a RedditApi object.

        This method is responsible for creating a new instance of the RedditApi class.
        
        Parameters:
            subreddit (str): The name of the subreddit to retrieve data from.
        
        Returns:
            RedditApi: The newly created RedditApi object.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.keyword = keyword
            cls._instance.start = start
            cls._instance.max_results = max_results
            cls._instance.create_query_string(keyword=cls._instance.keyword,
                                    start=cls._instance.start,
                                    max_results=cls._instance.max_results)

            cls._instance.url = None
            cls._instance.data = None
            
            cls._instance.base_url = 'http://export.arxiv.org/api/query'
        return cls._instance
    

    def get_data(self) -> dict | None:
        """
        Retrieves the data from the ArXiv API.
        
        Returns:
            dict | None: The parsed data from the API response, or None if the request failed.
        """
        response = requests.get(url=self._instance.base_url,
                                params=self._instance.query_params)
        if response.status_code == 200:
            self._instance.data = xmltodict.parse(response.content.decode())['feed']
            return self._instance.data['entry']
        else:
            return None
    
    def set_documents(self) -> list:
        """
        Sets the documents based on the retrieved data.
        
        Returns:
            list: A list of Document objects.
        """
        collection = list()
        if self._instance.data is None:
            self.get_data()

        entries = self._instance.data['entry']
        progress = 0
        total = len(entries)
        for document in entries:
            print_progress_bar(progress, total, 'Arxiv process')
            authors = [auth['name'] if isinstance(auth, dict) else auth for auth in document['author']]
            doc = ArxivDocument(title=document['title'],
                            date=datetime.datetime.strptime(document['published'], 
                                                            "%Y-%m-%dT%H:%M:%SZ").date(),
                            authors=authors,
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
            self._instance.keyword = kwargs['keyword']
        if 'start' in kwargs:
            self._instance.start = kwargs['start']
        if 'max_results' in kwargs:
            self._instance.start = kwargs['max_results']
            
        self.query_params = {
            'search_query': f'all:{self._instance.keyword}',
            'start': self._instance.start,
            'max_results': self._instance.max_results
            }
    