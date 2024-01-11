import re
import pickle
import pandas as pd
from pprint import pformat
from tabulate import tabulate
from modules.author import Author
from collections import defaultdict
from utils.tools import clean_paragraph
from modules.singleton import SingletonMeta
from collections import Counter
from typing import List, Tuple


class Corpus(metaclass=SingletonMeta):
    """
    Class representing a corpus of documents.
    """

    __concated_text = None

    def __init__(self):
        """
        Initialize a Corpus object.
        """
        # Mapping Variables
        self.authors = dict()
        self.documents = dict()
        self.__author_to_id = dict()
        self.__document_count = 0
        self.__author_count = 0

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
        if author not in self.__author_to_id:  # Setting up author unique ID
            self.__author_count += 1
            self.authors[self.__author_count] = Author(author)
            self.__author_to_id[author] = self.__author_count
        self.authors[self.__author_to_id[author]].add(doc.text)

        self.__document_count += 1
        self.documents[self.__document_count] = doc

    def __concat_data(self) -> None:
        """
        Concatenate all documents in the corpus if not concated.
        """
        if self.__concated_text is None:
            self.__concated_text = "".join([doc.text for doc in self.documents.values()])

    def search_text(self, keyword: str) -> List[Tuple[int, int, int]]:
        """
        Search for passages in the documents containing the given keyword.

        Args:
            keyword (str): The keyword to search for.

        Returns:
            list: A list of tuples containing the matched key word start, end 
                positions and document id.
        """
        self.__concat_data()

        matches = []
        for doc_id, doc in self.documents.items():
            match = re.finditer(keyword, doc.text)
            for m in match:
                matches.append((m.start(), m.end(), doc_id))

        return matches

    def __clean_text(self, doc:str=None) -> None:
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

        words = clean_paragraph(cleaned_doc)
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

    def docs_to_collection(self) -> List[str]:
        """
        Get all documents in the corpus in a list.
        Used as collection of all documents objects in the corpus.

        Returns:
            list: A list of documents.
        """
        return list(self.documents.values())

    def get_corpus_contents(self):
        """
        Get dictionary with just documents texts.

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
        if isinstance(int(doc_id), int):
            return self.documents[int(doc_id)]
        else:
            raise TypeError("Document ID must be an integer.")

    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert the corpus to a DataFrame.

        Returns:
            pd.DataFrame: A DataFrame representation of the corpus.
        """
        data = list()
        for doc_id, doc in self.documents.items():
            data.append({
                'id': doc_id,
                'title': doc.title,
                'text': doc.text,
                'author': doc.author,
                'date': doc.date,
                'source': doc.source,
                'url': doc.url
            })
        return pd.DataFrame(data)

    def from_pkl_file(self, path: str) -> None:
        """
        Load the corpus from a pickle file.

        Args:
            path (str): The path to the pickle file.
        """
        with open(path, 'rb') as file:
            data = pickle.load(file)
            self.documents = data['documents']
            self.authors = data['authors']
            self.__author_to_id = data['__author_to_id']
            
    
    def calculate_word_freq_per_year(self, words_to_track:List[str]) -> defaultdict:
        """
        Calculates the word frequency per year for the given list of words.

        Args:
            words_to_track (list): A list of words to track the frequency of.

        Returns:
            defaultdict: A nested defaultdict containing the word frequency per year.
        """
        word_freq_per_year = defaultdict(lambda: defaultdict(int))

        for doc in self.documents.values():
            try:
                date = doc.date
                year = date.year
            except (ValueError, AttributeError):
                continue

            text = (doc.text + ' ' + doc.title).lower()
            word_counter = Counter(text.split())

            for word in words_to_track:
                word_freq = word_counter[word.lower()]
                key = (word.lower(), str(year))
                if key in word_freq_per_year.keys():
                    word_freq += word_freq_per_year[key]
                word_freq_per_year[key] = word_freq

        return word_freq_per_year
