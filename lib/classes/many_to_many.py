class Article:
    all = []

    def __init__(self, author, magazine, title):
        if not isinstance(author, Author):
            raise Exception("Author must be an instance of Author")
        if not isinstance(magazine, Magazine):
            raise Exception("Magazine must be an instance of Magazine")

        self._author = author
        self._magazine = magazine
        self.title = title

        Article.all.append(self)

    # --- Properties ---

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # Enforce immutability
        if hasattr(self, '_title'):
            raise AttributeError("Title cannot be changed after the article is instantiated")

        if not isinstance(value, str):
            raise Exception("Title must be a string")
        if not 5 <= len(value) <= 50:
            raise Exception("Title must be between 5 and 50 characters, inclusive")

        self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise Exception("Author must be an instance of Author")
        self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if not isinstance(value, Magazine):
            raise Exception("Magazine must be an instance of Magazine")
        self._magazine = value

class Author:
    def __init__(self, name):
        self.name = name

    # --- Properties ---

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Enforce immutability
        if hasattr(self, '_name'):
            raise AttributeError("Author name cannot be changed after the author is instantiated")

        if not isinstance(value, str):
            raise Exception("Name must be a string")
        if not len(value) > 0:
            raise Exception("Name must be longer than 0 characters")

        self._name = value

    # --- Relationship Properties (for 34% and 38% tests) ---

    @property
    def articles(self):
        return [article for article in Article.all if article.author is self]

    @property
    def magazines(self):
        return list(set(article.magazine for article in self.articles))

    # --- Aggregate and Association Methods ---

    def add_article(self, magazine, title):
        if not isinstance(magazine, Magazine):
            raise Exception("Magazine must be an instance of Magazine")
        return Article(self, magazine, title)

    def topic_areas(self):
        if not self.articles:
            return None
        return list(set(magazine.category for magazine in self.magazines))

class Magazine:
    all = []

    def __init__(self, name, category):
        self.name = name
        self.category = category
        Magazine.all.append(self)

    # --- Properties ---

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise Exception("Name must be a string")
        if not 2 <= len(value) <= 16:
            raise Exception("Name must be between 2 and 16 characters, inclusive")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise Exception("Category must be a string")
        if not len(value) > 0:
            raise Exception("Category must be longer than 0 characters")
        self._category = value

    # --- Relationship Properties (for 76% and 80% tests) ---

    @property
    def articles(self):
        return [article for article in Article.all if article.magazine is self]

    @property
    def contributors(self):
        return list(set(article.author for article in self.articles))

    # --- Aggregate and Association Methods ---

    def article_titles(self):
        articles = self.articles
        return [article.title for article in articles] if articles else None

    def contributing_authors(self):
        articles = self.articles
        if not articles:
            return None

        author_counts = {}
        for article in articles:
            author = article.author
            author_counts[author] = author_counts.get(author, 0) + 1

        contributing = [author for author, count in author_counts.items() if count > 2]

        return contributing if contributing else None

    @classmethod
    def top_publisher(cls):
        if not Article.all:
            return None

        magazine_counts = {}
        for article in Article.all:
            magazine = article.magazine
            magazine_counts[magazine] = magazine_counts.get(magazine, 0) + 1

        # Returns the actual Magazine object with the highest count.
        return max(magazine_counts, key=magazine_counts.get)