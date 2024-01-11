import unittest

from modules.api import ArxivApi



class TestArxivAPI(unittest.TestCase):
    def setUp(self):
        arxiv_kw = 'machine learning'
        self.arxiv_obj = ArxivApi(keyword=arxiv_kw, max_results='2')
        
    def test_create_data(self):
        
        data = self.arxiv_obj.get_data()
        assert data is not None
        
    def test_set_documents(self):
        documents = self.arxiv_obj.set_documents()
        assert documents is not None

if __name__ == '__main__':
    unittest.main()