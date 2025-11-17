import pytest
from classes.many_to_many import Author, Magazine, Article

class TestArticle:

    def test_article_has_title(self):
        author = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        article = Article(author, magazine, "How to wear a tutu with style")
        assert article.title == "How to wear a tutu with style"

    def test_title_is_immutable_str(self):
        """title is an immutable string"""
        author = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        article_1 = Article(author, magazine, "How to wear a tutu with style")

        # trying to set a new title should raise AttributeError
        with pytest.raises(AttributeError):
            article_1.title = "New Title"

        with pytest.raises(AttributeError):
            article_1.title = 500  # invalid type

    def test_article_title_len(self):
        author = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        # valid title
        Article(author, magazine, "A valid title")  

        # invalid too short
        with pytest.raises(Exception):
            Article(author, magazine, "abc")  

        # invalid too long
        with pytest.raises(Exception):
            Article(author, magazine, "A" * 51)  

    def test_article_has_author(self):
        a = Author("Carry Bradshaw")
        m = Magazine("Vogue", "Fashion")
        article = Article(a, m, "Summer Fashion Tips")
        assert article.author == a

    def test_article_author_is_mutable(self):
        a1 = Author("Carry Bradshaw")
        a2 = Author("Bob")
        m = Magazine("Vogue", "Fashion")
        article = Article(a1, m, "Summer Fashion Tips")
        article.author = a2
        assert article.author == a2

    def test_article_has_magazine(self):
        a = Author("Carry Bradshaw")
        m = Magazine("Vogue", "Fashion")
        article = Article(a, m, "Summer Fashion Tips")
        assert article.magazine == m

    def test_article_magazine_is_mutable(self):
        a = Author("Carry Bradshaw")
        m1 = Magazine("Vogue", "Fashion")
        m2 = Magazine("AD", "Architecture")
        article = Article(a, m1, "Summer Fashion Tips")
        article.magazine = m2
        assert article.magazine == m2

    def test_article_class_has_all_attributes(self):
        a = Author("Carry Bradshaw")
        m = Magazine("Vogue", "Fashion")
        article = Article(a, m, "Summer Fashion Tips")
        assert hasattr(article, "title")
        assert hasattr(article, "author")
        assert hasattr(article, "magazine")
