# Run: python lib/debug.py
# Quick REPL to play with the domain

from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article
import ipdb

a1 = Author("Alice")
a2 = Author("Bob")

m1 = Magazine("TechDaily", "Technology")
m2 = Magazine("FoodieLife", "Food")

art1 = a1.add_article(m1, "Understanding Async IO in Python")
art2 = a1.add_article(m1, "Typing in Python: Pros and Cons")
art3 = a1.add_article(m2, "Baking Bread the Simple Way")
art4 = a2.add_article(m1, "Rust vs Python: A Pragmatic View")

ipdb.set_trace()
