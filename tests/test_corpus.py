import os
import unittest
import datetime

from modules.corpus import Corpus
from modules.document import RedditDocument

class TestCorpus(unittest.TestCase):
    def setUp(self):
        self.corpus = Corpus()
        self.todays_time = datetime.datetime.now().timestamp()
        self.title = 'test'
        self.author = 'test_author'
        self.date = datetime.datetime.fromtimestamp(self.todays_time)
        self.url = "https://test.com/"
        self.text = "lorem ipsum"
        self.num_comments = 2
        self.reddit_doc = RedditDocument(
            title=self.title,
            date=self.date,
            author=self.author,
            url=self.url,
            text=self.text,
            source='reddit',
            num_comments=self.num_comments,
        )
        

    def test_add_document(self):
        self.corpus.add(self.reddit_doc, 'Test Author')
        self.assertEqual(len(self.corpus.documents), 1)
        self.assertEqual(len(self.corpus.authors), 1)


    def test_search(self):
        matches = self.corpus.search_text('document')
        self.assertIsNotNone(matches)

    def test_stats(self):
        df = self.corpus.get_stats()
        self.assertIsNotNone(df)
        self.assertEqual(len(df), 4)

    def test_get_all_docs(self):
        docs = self.corpus.docs_to_collection()
        print(len(docs))
        self.assertIsInstance(docs, list)
        self.assertEqual(len(docs), 1)

if __name__ == '__main__':
    unittest.main()