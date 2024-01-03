import praw
import datetime
from config import reddit_auth
from modules.document import RedditDocument
from utils.tools import print_progress_bar


class RedditApi:
    _instance = None

    # Implementing singleton pattern
    def __new__(cls, subreddit):
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
                try:
                    cls._instance.reddit = praw.Reddit(
                        client_id=reddit_auth.client_id, 
                        client_secret=reddit_auth.client_secret, 
                        user_agent=reddit_auth.user_agent
                    )
                    cls._instance.subredit = subreddit
                    cls._instance.posts = list()
                    cls._instance.data = None
                    
                    return cls._instance
                
                except Exception as e:
                    print(e)
                    print("check 'config.py' file for reddit credentials")
    
    # def __init__(self, subreddit: str):
        
    #     self.reddit = praw.Reddit(
    #         client_id=reddit_auth.client_id, 
    #         client_secret=reddit_auth.client_secret, 
    #         user_agent=reddit_auth.user_agent
    #     )
    #     self.subredit = subreddit
    #     self.posts = list()
    #     self.data = None
    
    def get_data(self, limit=100) -> None:
        """
        Retrieves data from the specified subreddit.
        
        Parameters:
            limit (int): The maximum number of posts to retrieve. Default is 100.
        """
        self._instance.data = self._instance.reddit.subreddit(self._instance.subredit).hot(limit=limit)
    
    def set_documents(self) -> list:
        """
        Sets the documents using the retrieved data.
        
        Returns:
            list: A list of Document objects.
        """
        collection = list()
        if self._instance.data is None:
            self.get_data()

        progress = 0
        total = self._instance.data.limit
        for document in self._instance.data:
            print_progress_bar(progress, total, 'Reddit process')
            doc = RedditDocument(
                title=document.title,
                date=datetime.datetime.fromtimestamp(int(document.created)),
                author=document.author.name,
                url=document.url,
                text=str(document.selftext).replace('\n', ' '),
                num_comments=document.num_comments
            )
            collection.append(doc)
            progress += 1 
        return collection