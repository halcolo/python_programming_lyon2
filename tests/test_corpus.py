import os
import unittest
from modules.corpus import Corpus
from modules.document import Document

class TestCorpus(unittest.TestCase):
    def setUp(self):
        self.corpus = Corpus()
        self.doc = Document(
            title='Test Document', 
            text='lorem ipsum',
            author='Test Author',
            date='2020-01-01',
            url='https://test.com',
            )
        self.doc2 = Document(
            title='Test Document 2', 
            text='lorem ipsum 2', 
            author='Test Author 2',
            date='2020-01-02',
            url='https://test.com',
            )

    def test_add_document(self):
        self.corpus.add(self.doc, 'Test Author')
        self.assertEqual(len(self.corpus.id2doc), 1)
        self.assertEqual(len(self.corpus.authors), 1)
        self.assertEqual(self.corpus.ndoc, 1)
        self.assertEqual(self.corpus.author_num, 1)


    def test_search(self):
        self.corpus.add(self.doc, 'Test Author')
        matches = self.corpus.search('document')
        self.assertIsNotNone(matches)

    def test_clean_text(self):
        self.corpus.add(self.doc, 'Test Author')
        cleaned_doc = self.corpus.clean_text()
        self.assertIsNotNone(cleaned_doc)

    def test_stats(self):
        self.corpus.add(self.doc, 'Test Author')
        df = self.corpus.stats()
        self.assertIsNotNone(df)
        self.assertEqual(len(df), 3)

    def test_get_all_docs(self):
        self.corpus.add(self.doc, 'Test Author')
        docs = self.corpus.get_all_docs()
        self.assertEqual(len(docs), 3)

if __name__ == '__main__':
    unittest.main()