import requests
from bs4 import BeautifulSoup
import sys

sub_index = int(input())
url = input()

r = requests.get(url)

if r.status_code != 200:
    sys.exit()

soup = BeautifulSoup(r.content, 'html.parser')
all_headings = soup.find_all('h2')

print(all_headings[sub_index].text)
