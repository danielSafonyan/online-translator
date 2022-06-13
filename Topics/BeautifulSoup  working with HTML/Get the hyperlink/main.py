import requests
from bs4 import BeautifulSoup

hyper_index = int(input()) - 1
url = input()

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

all_links = soup.find_all('a')
required_link = all_links[hyper_index].get('href')

print(required_link)