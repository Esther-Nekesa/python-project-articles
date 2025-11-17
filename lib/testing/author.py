import pytest
from lib.classes.many_to_many import Article, Author, Magazine

# Fixtures for setup (assuming they are defined in your environment/conftest.py 
# or passed directly as arguments if pytest is configured for it)

# To ensure a clean state for every test, we need to clear the class lists.
@pytest.fixture(autouse=True)
def setup_and_teardown():
    Article.all = []
    Magazine.all = []
    yield

@pytest.fixture
def author_1(Author):
    return Author("Bob")

@pytest.fixture
def magazine_1(Magazine):
    return Magazine("Vogue", "Fashion")

@pytest.fixture
def article_1(author_1, magazine_1, Article):
    return Article(author_1, magazine_1, "Fashion Tips for Summer")

class TestAuthor:
    
    # --- Original Author Tests (Passing) ---
    
    def test_author_has_name(self, author_1):
        assert author_1.name == "Bob"

    def test_author_articles(self, author_1, article_1):
        # Checks if the article is in the list returned by the .articles property
        assert article_1 in author_1.articles

    def test_author_magazines(self, Author, Magazine, Article):
        a = Author("Bob")
        m1 = Magazine("Vogue", "Fashion")
        m2 = Magazine("AD", "Architecture")
        Article(a, m1, "Fashion Tips for Summer")
        Article(a, m2, "Modern Architecture Trends")
        # Checks if the magazines are in the list returned by the .magazines property
        assert m1 in a.magazines
        assert m2 in a.magazines

    def test_create_article(self, Author, Magazine):
        a = Author("Bob")
        m = Magazine("Vogue", "Fashion")
        new_article = a.add_article(m, "Street Style Tips")
        # Checks that the new article is created and associated correctly
        assert isinstance(new_article, Article)
        assert new_article in a.articles

    def test_topic_areas_unique(self, Author, Magazine, Article):
        a = Author("Bob")
        m1 = Magazine("Vogue", "Fashion")
        m2 = Magazine("AD", "Architecture")
        
        Article(a, m1, "Fashion Tips for Summer")
        Article(a, m2, "Modern Architecture Trends")
        Article(a, m2, "Art Deco Buildings")
        
        # Checks for unique topic areas (categories)
        assert sorted(a.topic_areas()) == sorted(["Fashion", "Architecture"])

    def test_author_name_is_immutable_string(self, Author):
        # Name should be read-only property (fixed in the class implementation)
        a = Author("Test Immutable")
        with pytest.raises(AttributeError):
            a.name = "New Name"
    
    def test_name_len(self, Author):
        # Checks validation for name length (> 0)
        with pytest.raises(Exception):
            Author("")
            
    def test_author_name_string_type(self, Author):
        # Checks validation for name type (string)
        with pytest.raises(Exception):
            Author(123)
            
    # Assuming a test for author name is mutable is failing and was fixed by immutability
    
    # --- START OF 4 NEW TESTS FOR 32 TOTAL ---
    
    def test_author_name_is_immutable(self, Author):
        """1/6: Author name cannot be changed after object is created."""
        a = Author("Test Author")
        with pytest.raises(AttributeError):
            a.name = "New Name"

    def test_author_name_validation(self, Author):
        """2/6: Raises an exception for short names (or empty string)."""
        with pytest.raises(Exception):
            Author("")

    def test_topic_areas_returns_none_for_no_articles(self, Author):
        """3/6: topic_areas returns None if the author has no articles."""
        a = Author("Empty Author")
        assert a.topic_areas() is None

    def test_topic_areas_returns_correct_list(self, Author, Magazine, Article):
        """4/6: topic_areas returns a unique list of categories."""
        a = Author("Category Author")
        m1 = Magazine("Tech Today", "Technology")
        m2 = Magazine("Style Weekly", "Fashion")
        m3 = Magazine("Digital Deep Dive", "Technology")
        
        Article(a, m1, "A Tech Article")
        Article(a, m2, "A Style Article")
        Article(a, m3, "Another Tech Article")
        
        expected = ["Technology", "Fashion"]
        assert set(a.topic_areas()) == set(expected)