import pytest
from lib.classes.many_to_many import Article, Author, Magazine

# Fixtures for setup (same as author_test.py, needed here too)
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

class TestMagazine:
    
    # --- Original Magazine Tests (Passing) ---
    
    def test_has_name(self, magazine_1):
        assert magazine_1.name == "Vogue"

    def test_name_is_mutable_string(self, magazine_1):
        magazine_1.name = "New Name"
        assert magazine_1.name == "New Name"
        
        with pytest.raises(Exception):
            magazine_1.name = 1
            
        with pytest.raises(Exception):
            magazine_1.name = " " # less than 2 chars
            
        with pytest.raises(Exception):
            magazine_1.name = "This name is too long for the validation" # more than 16 chars

    def test_name_len(self, Magazine):
        with pytest.raises(Exception):
            Magazine("x", "Category")
            
        with pytest.raises(Exception):
            Magazine("x" * 17, "Category")

    def test_has_category(self, magazine_1):
        assert magazine_1.category == "Fashion"

    def test_category_is_mutable_string(self, magazine_1):
        magazine_1.category = "Style"
        assert magazine_1.category == "Style"
        
        with pytest.raises(Exception):
            magazine_1.category = 1
            
    def test_category_len(self, Magazine):
        with pytest.raises(Exception):
            Magazine("Name", "") # length 0

    def test_has_many_articles(self, Magazine, Author, Article):
        m = Magazine("Vogue", "Fashion")
        a1 = Author("Bob")
        a2 = Author("Alice")
        Article(a1, m, "Summer Style")
        Article(a2, m, "Winter Style")
        assert len(m.articles) == 2

    def test_articles_of_type_articles(self, Magazine, Author, Article):
        m = Magazine("Vogue", "Fashion")
        a = Author("Bob")
        article = Article(a, m, "Fashion Tips")
        assert isinstance(m.articles[0], Article)

    def test_has_many_contributors(self, Magazine, Author, Article):
        m = Magazine("Vogue", "Fashion")
        a1 = Author("Bob")
        a2 = Author("Alice")
        Article(a1, m, "Summer Style")
        Article(a2, m, "Winter Style")
        contributors = m.contributors
        assert a1 in contributors
        assert a2 in contributors

    def test_contributors_are_unique(self, Magazine, Author, Article):
        m = Magazine("Vogue", "Fashion")
        a = Author("Bob")
        Article(a, m, "Tips 1")
        Article(a, m, "Tips 2")
        contributors = m.contributors
        assert len(contributors) == 1
        assert contributors[0] is a

    def test_article_titles(self, Magazine, Author, Article):
        m = Magazine("Vogue", "Fashion")
        a = Author("Bob")
        Article(a, m, "Tips 1")
        Article(a, m, "Tips 2")
        assert m.article_titles() == ["Tips 1", "Tips 2"]

    def test_contributing_authors(self, Magazine, Author, Article):
        m = Magazine("Vogue", "Fashion")
        a1 = Author("Bob")
        a2 = Author("Alice")
        
        # a1 has 3 articles (contributing)
        Article(a1, m, "A1 Tip 1")
        Article(a1, m, "A1 Tip 2")
        Article(a1, m, "A1 Tip 3") 
        
        # a2 has 2 articles (not contributing)
        Article(a2, m, "A2 Tip 1")
        Article(a2, m, "A2 Tip 2") 
        
        # The result should only include authors with > 2 articles
        contributing = m.contributing_authors()
        assert a1 in contributing
        assert a2 not in contributing
        assert len(contributing) == 1

    def test_top_publisher(self, Magazine, Author, Article):
        m1 = Magazine("Vogue", "Fashion")
        m2 = Magazine("AD", "Architecture")
        a = Author("Bob")
        
        # m1 has 2 articles
        Article(a, m1, "Fashion Tips")
        Article(a, m1, "More Fashion Tips")
        
        # m2 has 1 article
        Article(a, m2, "Architecture Guide")
        
        top = Magazine.top_publisher()
        assert top == m1
        
        # Test case where no articles exist
        Article.all.clear()
        assert Magazine.top_publisher() is None

    # --- START OF 2 NEW TESTS FOR 32 TOTAL ---
    
    def test_article_titles_returns_none_if_empty(self, Magazine):
        """5/6: article_titles returns None if there are no articles."""
        m = Magazine("Lonely Mag", "Niche")
        assert m.article_titles() is None

    def test_contributing_authors_returns_none_if_under_threshold(self, Magazine, Author, Article):
        """6/6: contributing_authors returns None if no author has 3+ articles."""
        m = Magazine("Boundary Mag", "Test")
        a1 = Author("One Article Author")
        a2 = Author("Two Articles Author")
        
        Article(a1, m, "Art 1")
        
        Article(a2, m, "Art 2")
        Article(a2, m, "Art 3")
        
        # a1 has 1 article, a2 has 2 articles. Neither is > 2.
        assert m.contributing_authors() is None