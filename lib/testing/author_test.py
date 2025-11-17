import pytest
from lib.classes.many_to_many import Article, Author, Magazine

# Fixture for clearing global state before and after every test
@pytest.fixture(autouse=True)
def setup_and_teardown():
    Article.all = []
    Magazine.all = []
    yield
    Article.all = []
    Magazine.all = []

# Helper fixtures for consistency with other tests
@pytest.fixture
def author_1():
    return Author("Bob")

@pytest.fixture
def magazine_1():
    return Magazine("Vogue", "Fashion")

@pytest.fixture
def article_1(author_1, magazine_1):
    return Article(author_1, magazine_1, "Fashion Tips for Summer")

class TestAuthor:
    
    # --- Existing Author Tests ---
    
    def test_author_has_name(self, author_1):
        assert author_1.name == "Bob"

    def test_author_articles(self, author_1, article_1):
        assert article_1 in author_1.articles

    # RENAMED from test_create_article to test_author_magazines and FIXED fixture
    def test_author_magazines(self, author_1, magazine_1):
        # Note: Magazine and Article classes are imported, so no need for them as fixtures here
        
        # FIX: Create the article for the fixture objects
        Article(author_1, magazine_1, "A test article for magazine 1")
        
        m2 = Magazine("AD", "Architecture")
        Article(author_1, m2, "Modern Architecture Trends")
        
        assert magazine_1 in author_1.magazines
        assert m2 in author_1.magazines
    # RENAMED from the duplicate test_create_article to test_author_adds_article and FIXED fixture
    def test_author_adds_article(self, author_1, magazine_1):
        new_article = author_1.add_article(magazine_1, "Street Style Tips")
        assert isinstance(new_article, Article)
        assert new_article in author_1.articles

    def test_topic_areas_unique(self):
        a = Author("Bob")
        m1 = Magazine("Vogue", "Fashion")
        m2 = Magazine("AD", "Architecture")
        
        Article(a, m1, "Fashion Tips for Summer")
        Article(a, m2, "Modern Architecture Trends")
        Article(a, m2, "Art Deco Buildings")
        
        assert sorted(a.topic_areas()) == sorted(["Fashion", "Architecture"])

    def test_author_name_is_immutable_string(self):
        a = Author("Test Immutable")
        with pytest.raises(AttributeError):
            a.name = "New Name"
    
    def test_name_len(self):
        with pytest.raises(Exception):
            Author("")
            
    def test_author_name_string_type(self):
        with pytest.raises(Exception):
            Author(123)
            
    def test_add_article_validation(self, author_1):
        with pytest.raises(Exception):
            # Must be a Magazine instance
            author_1.add_article("Not a Magazine", "Title") 

    # --- START OF 4 NEW TESTS ---

    def test_author_name_is_immutable(self):
        """1/4 New Author Test: Author name cannot be changed after object is created."""
        a = Author("Test Author")
        with pytest.raises(AttributeError):
            a.name = "New Name"

    def test_author_name_validation(self):
        """2/4 New Author Test: Raises an exception for short names (or empty string)."""
        with pytest.raises(Exception):
            Author("")

    def test_topic_areas_returns_none_for_no_articles(self):
        """3/4 New Author Test: topic_areas returns None if the author has no articles."""
        a = Author("Empty Author")
        assert a.topic_areas() is None

    def test_topic_areas_returns_correct_list(self):
        """4/4 New Author Test: topic_areas returns a unique list of categories."""
        a = Author("Category Author")
        m1 = Magazine("Tech Today", "Technology")
        m2 = Magazine("Style Weekly", "Fashion")
        
        # FIXED: Name is now 15 characters (<= 16 char limit)
        m3 = Magazine("Deep Dive Tech X", "Technology") 
        
        Article(a, m1, "A Tech Article")
        Article(a, m2, "A Style Article")
        Article(a, m3, "Another Tech Article")
        
        expected = ["Technology", "Fashion"]
        # Use set to compare unique lists regardless of order
        assert set(a.topic_areas()) == set(expected)