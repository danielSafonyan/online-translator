import requests
from bs4 import BeautifulSoup

word_to_search = input()
url = input()

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

all_paragraphs = soup.find_all('p')

texted_pars = [x.get_text() for x in all_paragraphs]

for paragraph in texted_pars:
    if word_to_search in paragraph:
        print(paragraph)
        break