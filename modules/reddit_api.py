import praw
import datetime
from utils.secrets import set_vars
from modules.Document import Document
from tools.progress_bar import print_progress_bar


reddit_auth = set_vars()
# print(reddit_auth)
class RedditApi:
    def __init__(self, subreddit: str):
        """
        Initializes a RedditApi object.
        
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
    
    def get_data(self, limit=100) -> None:
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

        progress = 0
        total = self.data.limit
        for document in self.data:
            print_progress_bar(progress, total, 'Reddit process')
            doc = Document(
                title=document.title,
                date=datetime.datetime.fromtimestamp(int(document.created)),
                author=[document.author.name],
                url=document.url,
                text=str(document.selftext).replace('\n', ' ')
            )
            collection.append(doc)
            progress += 1 
        return collection
        
        
            