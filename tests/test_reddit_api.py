import unittest
import json
import config
from modules.reddit_api import RedditApi

class TestRedditAPI(unittest.TestCase):
    def setUp(self):
        subreddit = 'MachineLearning'
        self.arxiv_obj = RedditApi(subreddit='MachineLearning')
        
    def test_set_documents(self):
        documents = self.arxiv_obj.set_documents()
        assert documents is not None
