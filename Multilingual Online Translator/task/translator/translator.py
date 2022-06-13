import requests
from bs4 import BeautifulSoup


def get_input():
    print('Type "en" if you want to translate from French into English, '
          'or "fr" if you want to translate from English '
          'into French:')
    target_language = input()

    print('Type the word you want to translate:')
    word_to_translate = input()

    print(f'You chose "{target_language}" as a language to translate "{word_to_translate}".')
    return target_language, word_to_translate


def make_request(target_language, word_to_translate):
    available_translation = {
        'en': 'french-english',
        'fr': 'english-french'
    }
    translation_type = available_translation[target_language]
    url = f'https://context.reverso.net/translation/{translation_type}/{word_to_translate}'

    while True:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            print('200 OK')
            break

    return r.content


def find_word_translations(content):
    soup = BeautifulSoup(content, 'html.parser')
    all_links = soup.select('a.translation.ltr.dict')
    word_translations = []
    for link in all_links:
        word = link.find('span', class_='display-term').get_text()
        word_translations.append(word)
    print(word_translations)


def find_word_usage_examples(content):
    soup = BeautifulSoup(content, 'html.parser')
    all_links = soup.find_all('div', class_='trg ltr')
    word_translations = []
    for link in all_links:
        word = link.find('span', class_='text').get_text()
        word = word.strip('\r\n ')
        word_translations.append(word)

    print(word_translations)


target_language, word_to_translate = get_input()
content = make_request(target_language, word_to_translate)
print("Translations")
find_word_translations(content)
find_word_usage_examples(content)








