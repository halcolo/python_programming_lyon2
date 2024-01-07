class Author:
    """
    Class representing an author.
    """
    def __init__(self, name: str) -> None:
        """
        Initialize an Author object.
        
        Parameters:
            name (str): The name of the author.
        """
        self.name = name
        self.production = list()
        self.nDoc = 0
    
    def __str__(self) -> str:
        """
        Return a string representation of the Author object.
        """
        return f'Author: {self.name} \tNumber of art:{self.nDoc}'
        
    def add(self, article: str) -> None:
        """
        Add an article to the author's production.
        
        Parameters:
            article (str): The article to add.
        """
        self.nDoc += 1 
        self.production.append(article)
        
