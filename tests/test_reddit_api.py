import unittest
import json
import config
import datetime
import time
from modules.reddit_api import RedditApi
from modules.document import RedditDocument

class TestRedditAPI(unittest.TestCase):
    def setUp(self):
        subreddit = 'MachineLearning'
        self.arxiv_obj = RedditApi(subreddit='MachineLearning')
        
    # def test_set_documents(self):
    #     documents = self.arxiv_obj.set_documents()
    #     assert documents is not None
        
    def test_reddit_document(self):
        todays_time = time.time() 
        document = RedditDocument(
                    title='test',
                    date=datetime.datetime.fromtimestamp(todays_time),
                    author='test_author',
                    url="https://test.com/",
                    text="lorem ipsum",
                    num_comments=0
                )

if __name__ == '__main__':
    unittest.main()