from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article
import ipdb

# Create Authors
author_1 = Author("Carrie Bradshaw")
author_2 = Author("Samantha Jones")
author_3 = Author("Charlotte York")

# Create Magazines
magazine_1 = Magazine("Vogue", "Fashion")
magazine_2 = Magazine("The New Yorker", "News")
magazine_3 = Magazine("House & Garden", "Home")

# Create Articles
# author_1: 4 articles total (3 in Vogue, 1 in New Yorker)
article_1 = author_1.add_article(magazine_1, "The Dress Dilemma")
article_2 = author_1.add_article(magazine_1, "Shoes and the City")
article_3 = author_1.add_article(magazine_1, "Finding Mr. Big")
article_4 = author_1.add_article(magazine_2, "Coffee Shop Review")

# author_2: 3 articles total (3 in New Yorker)
article_5 = author_2.add_article(magazine_2, "Dating in NYC: Part 1")
article_6 = author_2.add_article(magazine_2, "Dating in NYC: Part 2")
article_7 = author_2.add_article(magazine_2, "Dating in NYC: Part 3")

# author_3: 1 article total (1 in House & Garden)
article_8 = author_3.add_article(magazine_3, "Modern Art Deco")

print("\n--- Example Data Created ---")
print(f"Author 1: {author_1.name}")
print(f"Magazine 2: {magazine_2.name}, Category: {magazine_2.category}")
print(f"Article 5 Title: {article_5.title}")
print("--- Starting Debug Session ---")


# Start ipdb session for interactive testing
ipdb.set_trace()

# Example commands to run in ipdb:
# author_1.articles()
# author_1.magazines()
# author_1.topic_areas()
# magazine_2.articles()
# magazine_2.contributors()
# magazine_2.article_titles()
# magazine_2.contributing_authors() # Should return [author_2]
# Magazine.top_publisher() # Should return magazine_2