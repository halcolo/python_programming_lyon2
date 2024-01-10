import praw
import xmltodict
import datetime
import requests
from config import reddit_auth
from modules.document import ArxivDocument
from praw.exceptions import RedditAPIException
from modules.document import RedditDocument

class RedditApi:
    def __init__(self, subreddit, max_results=10):
        """
        Initializes the RedditApi object.

        This method is responsible for initializing the RedditApi object after it has been created.

        Args:
            subreddit (str): The name of the subreddit to retrieve data from.
        """
        self.reddit = praw.Reddit(
            client_id=reddit_auth.client_id,
            client_secret=reddit_auth.client_secret,
            user_agent=reddit_auth.user_agent
        )
        self.subreddit = subreddit
        self.posts = list()
        self.data = list()
        self.max_results = max_results
    

    def get_data(self):
        """
        Retrieves data from the specified subreddit.
        
        Args:
            limit (int): The maximum number of posts to retrieve. Default is 10.
        
        Returns:
            praw.models.ListingGenerator: A generator object containing the retrieved posts.
        """
        try:
            self.data = self.reddit.subreddit(self.subreddit).hot(limit=self.max_results)
            return self.data
        except RedditAPIException as e:
            raise ValueError(f'Error retrieving data: {e}')
        except Exception as e:
            raise ValueError(f'Error retrieving data: {e}')
    

    def check_data(self):
        """
        Checks if the data collection is available.
        If the data is not available, it retrieves it.
        """
        if isinstance(self.data, list) and len(self.data) == 0:
            self.get_data()
        
    def set_documents(self):
        """
        Sets the documents using the retrieved data.
        
        Returns:
            list: A list of Document objects.
        """
        collection = list()
        self.check_data()
        
        if self.data is None:
            raise ValueError('No data found. Check your credentials.')
        
        for document in self.data:
            if document is not None:
                collection.append(RedditDocument.from_praw(document))
        
        return collection
    
    
class ArxivApi:
    
    def __init__(self, keyword: str, start: int = 0, max_results: int = 1) -> None:
        """
        Initializes an ArxivApi object.

        This method is responsible for creating a new instance of the ArxivApi class.
        
        Args::
            keyword (str): The keyword to search for.
            start (int): The starting index of the search results.
            max_results (int): The maximum number of results to retrieve.
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
        self.session = requests.Session()
    
    def get_data(self) -> dict | None:
        """
        Retrieves the data from the ArXiv API.
        
        Returns:
            dict | None: The parsed data from the API response, or None if the request failed.
        """
        try:
            response = self.session.get(url=self.base_url, params=self.query_params)
            if response.status_code == 200:
                self.data = xmltodict.parse(response.content.decode())['feed']
                if 'entry' not in self.data:
                    raise ValueError('No data founded from ARXIV API')
                else:
                    return self.data['entry']
        except requests.RequestException:
            pass
        return None
    
    def set_documents(self) -> list:
        """
        Sets the documents based on the retrieved data.
        
        Returns:
            list: A list of Document objects.
        """
        if self.data is None:
            self.get_data()

        entries = self.data['entry']
        collection = [
            ArxivDocument(
                title=document['title'],
                date=datetime.datetime.strptime(document['published'], "%Y-%m-%dT%H:%M:%SZ").date(),
                authors=[auth['name'] if isinstance(auth, dict) else auth for auth in document['author']],
                url=document['id'],
                source='arxiv'.lower(),
                text=str(document['summary']).replace('\n',' ')
            )
            for document in entries
        ]
        return collection
    
    def create_query_string(self, **kwargs) -> None:
        """
        Creates the query string for the ArXiv API request.
        
        Args::
            **kwargs: The keyword arguments to update the query Args:.
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
