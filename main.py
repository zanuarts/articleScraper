import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import xlsxwriter

# Cannot proceed from other link

url = 'https://www.kompasiana.com/tag/karir'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

article_titles, article_authors, article_dates, article_links, article_contents = [], [], [], [], []

for tag in soup.findAll("div", {"class": "artikel"}):
    tag_title = tag.find("h2")
    tag_author = tag.find("div", {"class":"user-box"}).find("a")
    tag_date = tag.find("div", {"class":"date-box"})
    tag_link = tag.find("h2").find("a")

    article_title = tag_title.get_text().strip()
    article_author = tag_author.get_text()
    article_date = tag_date.get_text().strip()
    article_link = tag_link["href"]

    article_titles.append(article_title)
    article_authors.append(article_author)
    article_dates.append(article_date)
    article_links.append(article_link)

    # reading article
    article = requests.get(article_link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, "html.parser")
    body = soup_article.find_all("div", {"class": "read-content"})
    x = body[0].find_all("p")

    # menyatukan paragraph
    list_p = []
    for p in np.arange(0, len(x)):
      paragraph = x[p].get_text()
      list_p.append(paragraph)
      final_article = " ".join(list_p)

    article_contents.append(final_article)

df = pd.DataFrame({
    "title":article_titles, 
    "author":article_authors, 
    "date created":article_dates, 
    "link content":article_links,
    "content":article_contents,
})

def create_document(worksheet, df):
  for idx, col in enumerate(df):
    series = df[col]
    max_len = (
        max((
          series.astype(str).map(len).max(),
          len(str(series.name)),
        ))+1
    )
    worksheet.set_column(idx, idx, max_len)

writer = pd.ExcelWriter("Artikel_Karir.xlsx",engine="xlsxwriter")
df.to_excel(writer, sheet_name="Sheet 1", index=False)
create_document(writer.sheets["Sheet 1"], df)
writer.save()