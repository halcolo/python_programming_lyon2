import datetime
import requests
import xmltodict

class Document:
    """
    Class representing a document.
    """
    def __init__(self,
                 title: str,
                 date: str,
                 author: str,
                 url: str,
                 source: str,
                 text: str) -> None:
        """
        Initialize a Document object.
        
        Args::
            title (str): The title of the document.
            date (str): The date of the document.
            author (str): The author of the document.
            url (str): The URL of the document.
            text (str): The text of the document.
        """
        self.title = title
        self.date = date
        self.author = author
        self.url = url
        self.text = text
        self.source = source
        
    def __repr__(self) -> str:
        """
        Return a string representation of the Document object.
        """
        return  f"Title: {self.title}\t" \
                f"Author: {self.author}\t" \
                f"Date: {self.date}\t" \
                f"URL: {self.url}\t" \
                f"Text: {self.text}\t" \
                f"Source: {self.source}\t"

    def __str__(self) -> str:
        """
        Return a string representation of the Document object.
        """
        if isinstance(self.author, list):
            author = ' '.join(self.author)
        else:
            author = self.author
        resp =  f"{self.title}, by Authors: {author}, "\
                f"on Date: {self.date}, at URL: {self.url}, "\
                f"From: {self.source}, with Text: {self.text}"
        return resp


class RedditDocument(Document):
    """
    Class representing a Reddit document.
    """
    def __init__(self,
                 title: str,
                 date: str,
                 author: str,
                 url: str,
                 text: str,
                 source: str,
                 num_comments: int) -> None:
        """
        Initialize a RedditDocument object.
        
        Args::
            title (str): The title of the document.
            date (str): The date of the document.
            author (str): The author of the document.
            url (str): The URL of the document.
            text (str): The text of the document.
            num_comments (int): The number of comments on the document.
        """
        super().__init__(title, date, author, url, source.lower(), text)
        self.num_comments = num_comments

    def __str__(self) -> str:
        """
        Return a string representation of the RedditDocument object.
        """
        return super().__str__() + f", with {self.num_comments} comments"
    
    
    @classmethod
    def from_praw(cls, praw_document):
        if praw_document.author is not None:
            if praw_document.author is not None:
                aut_name = praw_document.author.name if praw_document.author.name is not None else 'Anonymous'
            else:
                aut_name = 'Anonymous'
            return cls(
                title=praw_document.title,
                date=datetime.datetime.fromtimestamp(int(praw_document.created)),
                author=aut_name,
                url=praw_document.url,
                text=str(praw_document.selftext).replace('\n', ' '),
                source='reddit'.lower(), # Source in lowr case
                num_comments=praw_document.num_comments
            )

class ArxivDocument(Document):
    """
    Class representing an Arxiv document.
    """
    def __init__(self,
                 title: str,
                 date: str,
                 authors: list,
                 url: str,
                 source: str,
                 text: str,) -> None:
        """
        Initialize an ArxivDocument object.
        
        Args::
            title (str): The title of the document.
            date (str): The date of the document.
            authors (list): The authors of the document.
            url (str): The URL of the document.
            text (str): Abstract of the document.
        """
        super().__init__(title, date, ', '.join(authors), url, source, text)

    def __str__(self) -> str:
        """
        Return a string representation of the ArxivDocument object.
        """
        return super().__str__()
