import re
import pandas as pd
from pprint import pformat
from tabulate import tabulate
from modules.author import Author
from utils.tools import clean_text_util
# from utils.tools import singleton


# @singleton
class Corpus:
    """
    Class representing a corpus of documents.
    """

    __concated_text = None

    def __init__(self, name: str = 'Corpus 1'):
        """
        Initialize a Corpus object.

        Args:
            name (str): The name of the corpus.
        """
        self.name = name
        # Author ID to Author mapping
        self.authors = dict()
        # Document ID to document mapping
        self.documents = dict()
        # Author to ID mapping
        self.author_to_id = dict()
        # Number of documents
        self.document_count = 0
        # Number of authors
        self.author_count = 0

    def __repr__(self):
        """
        Returns:
            String representation of the Corpus object.
        """
        return pformat(self.get_stats(), indent=4, width=1)

    def __str__(self):
            """
            Returns a string representation of the Corpus object.
            
            The string representation includes the statistics of the Corpus object
            in a tabulated format.
            
            Returns:
                str: A string representation of the Corpus object.
            """
            stats = self.get_stats()
            return tabulate(list(stats.items()))

    def add(self, doc, author):
        """
        Add a document to the corpus.

        Args:
            doc: The document to add.
            author: The author of the document.
        """
        if author not in self.author_to_id: # Setting up author unique ID
            self.author_count += 1
            self.authors[self.author_count] = Author(author)
            self.author_to_id[author] = self.author_count
        self.authors[self.author_to_id[author]].add(doc.text)

        self.document_count += 1
        self.documents[self.document_count] = doc


    def __concat_data(self) -> None:
        """
        Concatenate all documents in the corpus if not concated.
        """
        if self.__concated_text is None:
            self.__concated_text = "".join([doc.text for doc in self.documents.values()])

    def search_text(self, keyword: str) -> list:
        """
        Search for passages in the documents containing the given keyword.

        Args:
            keyword (str): The keyword to search for.

        Returns:
            list: A list of tuples containing the matched key word start, end positions and document id.
        """
        self.__concat_data()

        matches = []
        for doc_id, doc in self.documents.items():
            match = re.finditer(keyword, doc.text)
            for m in match:
                matches.append((m.start(), m.end(), doc_id))

        return matches

    def __clean_text(self, doc:str = None) -> None:
        """
        Clean the text of a document.

        Args:
            doc (str): The document to clean. If None, clean the entire corpus.

        Returns:
            str: The cleaned document.
        """

        if doc is None:
            self.__concat_data()
            cleaned_doc = self.__concated_text

        else:
            cleaned_doc = doc

        words = clean_text_util(cleaned_doc)
        cleaned_doc = ' '.join(words)

        return cleaned_doc

    def get_stats(self) -> pd.DataFrame:
        """
        Calculate statistics about the corpus.

        Returns:
            pd.DataFrame: A DataFrame containing the statistics.
        """
        cleaned_doc = self.__clean_text()
        words = list()
        count = list()
        counter_docs = list()
        splited_text = list()
        ids = list()
        counter = 0
        for doc in self.documents:
            splited_text.append(self.__clean_text(self.documents[doc].text).split(' '))

        splited_text.sort()  # Sort the splited_text list alphabetically

        for word in set(cleaned_doc.split(' ')):
            counter += 1
            ids.append(counter)
            words.append(word)
            count.append(cleaned_doc.count(word))
            counter_docs.append(sum([1 for doc in splited_text if word in doc]))

        data = {'id': ids, 'word': words, 'count': count, 'counter_docs': counter_docs}

        return data

    def get_all_docs(self) -> list:
        """
        Get all documents in the corpus.

        Returns:
            list: A list of documents.
        """
        return list(self.documents.values())
    
    def all_docs(self):
        """
        Get all documents in the corpus.

        Returns:
            list: A list of documents.
        """
        documents = dict()
        for id, doc in self.documents.items():
            documents[id] = doc.text
        return documents
    
    def get_document(self, doc_id: int) -> str:
        """
        Get a document from the corpus.

        Args:
            doc_id (int): The ID of the document to get.

        Returns:
            str: The document.
        """
        return self.documents[doc_id]  
    
    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert the corpus to a DataFrame.

        Returns:
            pd.DataFrame: A DataFrame representation of the corpus.
        """
        data = list()
        for doc_id, doc in self.documents.items():
            data.append({'id': doc_id, 'title': doc.title, 'text': doc.text, 'author': doc.author, 'date': doc.date})
        return pd.DataFrame(data)
