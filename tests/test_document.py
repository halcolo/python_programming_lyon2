
import unittest
import datetime
from modules.document import RedditDocument, ArxivDocument


class TestRedditDocument(unittest.TestCase):
    def setUp(self):
        self.todays_time = datetime.datetime.now().timestamp()
        self.todays_time = datetime.datetime.now().timestamp()
        self.title = 'test'
        self.author = 'test_author'
        self.date = datetime.datetime.fromtimestamp(self.todays_time)
        self.url = "https://test.com/"
        self.text = "lorem ipsum"
        self.num_comments=2
        self.document = RedditDocument(
            title=self.title,
            date=self.date,
            author=self.author,
            url=self.url,
            text=self.text,
            num_comments=self.num_comments,
        )
        
    def test_init(self):
        self.assertEqual(self.document.title, 'test')
        self.assertEqual(self.document.date, datetime.datetime.fromtimestamp(self.todays_time))
        self.assertEqual(self.document.author, 'test_author')
        self.assertEqual(self.document.url, 'https://test.com/')
        self.assertEqual(self.document.text, 'lorem ipsum')
        self.assertEqual(self.document.num_comments, 2)
        
    def test_str(self):
        expected_output = f"{self.title}, by Authors: {self.author}, "\
            f"on Date: {self.date}, at URL: {self.url}, " \
            f"with Text: {self.text}, " \
            f"with {self.num_comments} comments"
        # print(str(self.document))
        self.assertEqual(str(self.document), expected_output)
        
class TestArxivDocument(unittest.TestCase):
    def setUp(self):
        self.todays_time = datetime.datetime.now().timestamp()
        self.title = 'test'
        self.author = 'test_author'
        self.date = datetime.datetime.fromtimestamp(self.todays_time)
        self.url = "https://test.com/"
        self.text = "lorem ipsum"
        
        self.document = ArxivDocument(
            title=self.title,
            date=self.date,
            authors=[self.author],
            url=self.url,
            text=self.text
        )
        
    def test_init(self):
        self.assertEqual(self.document.title, 'test')
        self.assertEqual(self.document.date, datetime.datetime.fromtimestamp(self.todays_time))
        self.assertEqual(self.document.author, 'test_author')
        self.assertEqual(self.document.url, 'https://test.com/')
        self.assertEqual(self.document.text, 'lorem ipsum')
        
    def test_str(self):
        expected_output = f"{self.title}, by Authors: {self.author}, "\
            f"on Date: {self.date}, at URL: {self.url}, " \
            f"with Text: {self.text}"
        self.assertEqual(str(self.document), expected_output)