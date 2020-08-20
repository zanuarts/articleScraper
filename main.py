import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.kompasiana.com/tag/etika'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# print(response.text)

article_titles, article_authors = [], []

for tag in soup.findAll("div", {"class": "artikel"}):
    tag_title = tag.find("h2")
    tag_author = tag.find("div", {"class":"user-box"}).find_all("a")

    article_title = tag_title.get_text().strip()
    article_author = tag_author

    article_titles.append(article_title)
    article_authors.append(article_author)

df = pd.DataFrame({"title":article_titles, "author":article_authors})
df.shape

df.head()