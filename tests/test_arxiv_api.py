import unittest
import json
from modules.arxiv_api import ArxivApi

class TestArxivAPI(unittest.TestCase):
    def setUp(self):
        print('GET ARXIV DATA')
        arxiv_kw = 'machine learning'
        self.arxiv_obj = ArxivApi(keyword=arxiv_kw, max_results='2')
        
    def test_create_data(self):
        
        data = self.arxiv_obj.get_data()
        assert data is not None
        
    def test_set_documents(self):
        documents = self.arxiv_obj.set_documents()
        assert documents is not None
