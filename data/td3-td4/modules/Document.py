class Document:
    """
    Class representing a document.
    """
    def __init__(self, title: str, date: str, author: str, url: str, text: str) -> None:
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
        return f"{self.title}, by {author}"

    