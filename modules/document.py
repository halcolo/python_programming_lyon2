class Document:
    """
    Class representing a document.
    """
    def __init__(self,
                 title: str,
                 date: str,
                 author: str,
                 url: str,
                 text: str) -> None:
        """
        Initialize a Document object.
        
        Parameters:
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
        
    def __repr__(self) -> str:
        """
        Return a string representation of the Document object.
        """
        return f"Title: {self.title}\t" \
               f"Author: {self.author}\t" \
               f"Date: {self.date}\t" \
               f"URL: {self.url}\t" \
               f"Text: {self.text}\t"

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
                f"with Text: {self.text}"
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
                 num_comments: int) -> None:
        """
        Initialize a RedditDocument object.
        
        Parameters:
            title (str): The title of the document.
            date (str): The date of the document.
            author (str): The author of the document.
            url (str): The URL of the document.
            text (str): The text of the document.
            num_comments (int): The number of comments on the document.
        """
        super().__init__(title, date, author, url, text)
        self.num_comments = num_comments

    def __str__(self) -> str:
        """
        Return a string representation of the RedditDocument object.
        """
        return super().__str__() + f", with {self.num_comments} comments"


class ArxivDocument(Document):
    """
    Class representing an Arxiv document.
    """
    def __init__(self,
                 title: str,
                 date: str,
                 authors: list,
                 url: str,
                 text: str) -> None:
        """
        Initialize an ArxivDocument object.
        
        Parameters:
            title (str): The title of the document.
            date (str): The date of the document.
            authors (list): The authors of the document.
            url (str): The URL of the document.
            text (str): Abstract of the document.
        """
        super().__init__(title, date, ', '.join(authors), url, text)

    def __str__(self) -> str:
        """
        Return a string representation of the ArxivDocument object.
        """
        return super().__str__()
