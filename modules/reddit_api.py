import praw
import datetime
from config import reddit_auth
from modules.document import RedditDocument
from utils.tools import print_progress_bar, singleton


# @singleton
class RedditApi:
    def __init__(self, subreddit):
        """
        Initializes the RedditApi object.

        This method is responsible for initializing the RedditApi object after it has been created.

        Parameters:
            subreddit (str): The name of the subreddit to retrieve data from.
        """
        self.reddit = praw.Reddit(
            client_id=reddit_auth.client_id,
            client_secret=reddit_auth.client_secret,
            user_agent=reddit_auth.user_agent
        )
        self.subredit = subreddit
        self.posts = list()
        self.data = None
    
    def get_data(self, limit=10) -> None:
        """
        Retrieves data from the specified subreddit.
        
        Parameters:
            limit (int): The maximum number of posts to retrieve. Default is 100.
        """
        self.data = self.reddit.subreddit(self.subredit).hot(limit=limit)
    
    def set_documents(self) -> list:
        """
        Sets the documents using the retrieved data.
        
        Returns:
            list: A list of Document objects.
        """
        collection = list()
        if self.data is None:
            self.get_data()

        for document in self.data:
            if type(document) is not None:
                aut_name = document.author.name if document.author.name is not None else 'Anonymous'
                doc = RedditDocument(
                    title=document.title,
                    date=datetime.datetime.fromtimestamp(int(document.created)),
                    author=aut_name,
                    url=document.url,
                    text=str(document.selftext).replace('\n', ' '),
                    num_comments=document.num_comments
                )
                collection.append(doc)
        return collection