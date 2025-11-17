class Article:
    # Class attribute to keep track of all articles
    all = []

    def __init__(self, author, magazine, title):
        # Validate author, magazine, and title upon initialization
        if not isinstance(author, Author):
            raise TypeError("Author must be an instance of Author")
        if not isinstance(magazine, Magazine):
            raise TypeError("Magazine must be an instance of Magazine")
        
        self._author = author
        self._magazine = magazine
        
        # Setter for title handles validation
        self.title = title
        
        Article.all.append(self)

    # --- Properties ---

    @property
    def title(self):
        """Returns the article's title. Read-only after instantiation."""
        return self._title

    @title.setter
    def title(self, value):
        """Sets the article's title with validation."""
        if hasattr(self, '_title'):
            # Title cannot be changed after instantiation
            raise AttributeError("Title cannot be changed after the article is instantiated")
        
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        if not 5 <= len(value) <= 50:
            raise ValueError("Title must be between 5 and 50 characters, inclusive")
        
        self._title = value

    @property
    def author(self):
        """Returns the author object for the article."""
        return self._author

    @author.setter
    def author(self, value):
        """Sets the author object with validation."""
        if not isinstance(value, Author):
            raise TypeError("Author must be an instance of Author")
        self._author = value

    @property
    def magazine(self):
        """Returns the magazine object for the article."""
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        """Sets the magazine object with validation."""
        if not isinstance(value, Magazine):
            raise TypeError("Magazine must be an instance of Magazine")
        self._magazine = value

# Import necessary classes for type checking and relationships
# These imports are typically placed at the top of the file in a real project,
# but for the sake of a single runnable block, they are placed here.
from .author import Author
from .magazine import Magazine