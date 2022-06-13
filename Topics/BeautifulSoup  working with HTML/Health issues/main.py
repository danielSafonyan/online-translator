import requests
from bs4 import BeautifulSoup

letter = 'S'
url = input()

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

all_links = soup.find_all('a')
wanted_links = []

for link in all_links:
    hyper_link = link.get('href')
    try:
        if 'topics' in hyper_link or 'entity' in hyper_link:
                link_text = link.text
                if link_text.startswith(letter) and len(link_text) > 1:
                    wanted_links.append(link_text)
    except Exception:
        continue

print(wanted_links)



