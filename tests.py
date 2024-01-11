import unittest
from modules.arxiv_api import ArxivApi

class TestArxivApi(unittest.TestCase):
    def setUp(self):
        self.keyword = "machine learning"
        self.start = 0
        self.max_results = 1
        self.api = ArxivApi(self.keyword, self.start, self.max_results)

    def test_get_data(self):
        data = self.api.get_data()
        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)

    def test_set_documents(self):
        documents = self.api.set_documents()
        self.assertIsNotNone(documents)
        self.assertIsInstance(documents, list)
        self.assertGreater(len(documents), 0)
        for document in documents:
            self.assertIsNotNone(document.title)
            self.assertIsNotNone(document.date)
            self.assertIsNotNone(document.authors)
            self.assertIsNotNone(document.url)
            self.assertIsNotNone(document.text)

    def test_create_query_string(self):
        keyword = "deep learning"
        start = 10
        max_results = 5
        self.api.create_query_string(keyword=keyword, start=start, max_results=max_results)
        # self.assertEqual(self.api.keyword, keyword)
        # self.assertEqual(self.api.start, start)
        # self.assertEqual(self.api.max_results, max_results)
        self.assertEqual(self.api.query_params['search_query'], f'all:{keyword}')
        self.assertEqual(self.api.query_params['start'], start)
        self.assertEqual(self.api.query_params['max_results'], max_results)

if __name__ == '__main__':
    unittest.main()