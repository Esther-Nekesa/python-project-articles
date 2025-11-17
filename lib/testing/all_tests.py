import pytest
from classes.many_to_many import Article, Author, Magazine

# ----------------- ARTICLE TESTS -----------------
class TestArticle:
    def test_article_has_title(self):
        author = Author("Alice")
        magazine = Magazine("Vogue", "Fashion")
        article = Article(author, magazine, "Summer Fashion Tips")
        assert article.title == "Summer Fashion Tips"

    def test_title_is_immutable(self):
        author = Author("Alice")
        magazine = Magazine("Vogue", "Fashion")
        article = Article(author, magazine, "Summer Fashion Tips")
        with pytest.raises(AttributeError):
            article.title = "New Title"

    def test_article_author_magazine(self):
        author = Author("Alice")
        magazine = Magazine("Vogue", "Fashion")
        article = Article(author, magazine, "Summer Fashion Tips")
        assert article.author == author
        assert article.magazine == magazine

# ----------------- AUTHOR TESTS -----------------
class TestAuthor:
    def test_author_has_name(self):
        author = Author("Bob")
        assert author.name == "Bob"

    def test_author_articles(self):
        a = Author("Bob")
        m = Magazine("Vogue", "Fashion")
        art = a.create_article(m, "Street Style Tips")
        assert art in a.articles()

    def test_author_magazines(self):
        a = Author("Bob")
        m1 = Magazine("Vogue", "Fashion")
        m2 = Magazine("AD", "Architecture")
        a.create_article(m1, "Street Style Tips")
        a.create_article(m2, "Modern Architecture")
        assert m1 in a.magazines()
        assert m2 in a.magazines()

    def test_create_article(self):
        a = Author("Bob")
        m = Magazine("Vogue", "Fashion")
        new_article = a.create_article(m, "Street Style Tips")
        assert isinstance(new_article, Article)
        assert new_article.author == a
        assert new_article.magazine == m
        assert new_article.title == "Street Style Tips"

    def test_topic_areas_unique(self):
        a = Author("Bob")
        m1 = Magazine("Vogue", "Fashion")
        m2 = Magazine("AD", "Fashion")
        a.create_article(m1, "Street Style Tips")
        a.create_article(m2, "Modern Architecture")
        topics = a.topic_areas()
        assert "Fashion" in topics
        assert len(topics) == len(set(topics))

# ----------------- MAGAZINE TESTS -----------------
class TestMagazine:
    def test_has_name(self):
        m = Magazine("Vogue", "Fashion")
        assert m.name == "Vogue"

    def test_name_is_mutable_string(self):
        m = Magazine("Vogue", "Fashion")
        m.name = "New Yorker"
        assert m.name == "New Yorker"

    def test_name_len(self):
        m = Magazine("Vogue", "Fashion")
        with pytest.raises(Exception):
            m.name = "A"  # too short
        with pytest.raises(Exception):
            m.name = "X" * 20  # too long

    def test_has_category(self):
        m = Magazine("Vogue", "Fashion")
        assert m.category == "Fashion"

    def test_category_is_mutable_string(self):
        m = Magazine("Vogue", "Fashion")
        m.category = "Lifestyle"
        assert m.category == "Lifestyle"

    def test_category_len(self):
        m = Magazine("Vogue", "Fashion")
        with pytest.raises(Exception):
            m.category = ""  # cannot be empty

    def test_has_many_articles(self):
        a = Author("Alice")
        m = Magazine("Vogue", "Fashion")
        art1 = Article(a, m, "Summer Fashion Trends")
        art2 = Article(a, m, "Winter Fashion Trends")
        assert len(m.articles()) == 2
        assert art1 in m.articles()
        assert art2 in m.articles()

    def test_articles_of_type_articles(self):
        a = Author("Alice")
        m = Magazine("Vogue", "Fashion")
        art1 = Article(a, m, "Summer Fashion Trends")
        assert isinstance(m.articles()[0], Article)

    def test_has_many_contributors(self):
        a1 = Author("Alice")
        a2 = Author("Bob")
        m = Magazine("Vogue", "Fashion")
        Article(a1, m, "Summer Fashion Trends")
        Article(a2, m, "Winter Fashion Trends")
        assert len(m.contributors()) == 2
        assert a1 in m.contributors()
        assert a2 in m.contributors()

    def test_contributors_are_unique(self):
        a1 = Author("Alice")
        m = Magazine("Vogue", "Fashion")
        Article(a1, m, "Summer Fashion Trends")
        Article(a1, m, "Winter Fashion Trends")
        assert len(m.contributors()) == 1  # unique contributors

    def test_article_titles(self):
        a = Author("Alice")
        m = Magazine("Vogue", "Fashion")
        Article(a, m, "Summer Fashion Trends")
        Article(a, m, "Winter Fashion Trends")
        titles = m.article_titles()
        assert "Summer Fashion Trends" in titles
        assert "Winter Fashion Trends" in titles

    def test_contributing_authors(self):
        a = Author("Alice")
        m = Magazine("Vogue", "Fashion")
        Article(a, m, "Summer Fashion Trends")
        Article(a, m, "Winter Fashion Trends")
        contribs = m.contributing_authors()
        assert a in contribs

    def test_top_publisher(self):
        # Reset all data
        Magazine.all = []
        Article.all = []
        a = Author("Alice")
        m1 = Magazine("Vogue", "Fashion")
        m2 = Magazine("AD", "Architecture")
        Article(a, m1, "Summer Fashion Trends")
        Article(a, m1, "Winter Fashion Trends")
        Article(a, m1, "Street Style Tips")
        Article(a, m2, "Modern Architecture")
        top = Magazine.top_publisher()
        assert top == m1
        assert isinstance(top, Magazine)
