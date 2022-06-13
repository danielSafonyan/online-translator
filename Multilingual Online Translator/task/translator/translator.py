import requests
from bs4 import BeautifulSoup

supported_languages = 'Arabic German English Spanish French ' \
                      'Hebrew Japanese Dutch Polish ' \
                      'Portuguese Romanian Russian Turkish'.lower().split()
dict_supported_languages = {str(idx + 1): language for idx, language in enumerate(supported_languages)}


def welcoming_message():
    print('Hello, welcome to the translator. Translator supports: ')
    for key in dict_supported_languages:
        print(f"{key}. {dict_supported_languages[key].title()}")

def get_input():
    print('Type the number of your language:')
    src_language = input()

    print('Type the number of language you want to translate to:')
    trgt_language = input()

    print('Type the word you want to translate:')
    word_to_translate = input()

    return dict_supported_languages[src_language], dict_supported_languages[trgt_language], word_to_translate


def make_request(src_language, trgt_language, word_to_translate):
    url = f'https://context.reverso.net/translation/{src_language}-{trgt_language}/{word_to_translate}'

    while True:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            print()
            break

    return r.content


def find_word_translations(content):
    soup = BeautifulSoup(content, 'html.parser')
    all_links = soup.select('a.translation.ltr.dict')
    word_translations = []
    for link in all_links:
        word = link.find('span', class_='display-term').get_text()
        word_translations.append(word)

    print(f"{trgt_language} Translations")

    for word in word_translations:
        print(word)

    print()


def find_word_usage_examples(content):
    soup = BeautifulSoup(content, 'html.parser')

    all_links = soup.find_all('div', class_='src ltr')
    src_usage_examples = []
    for link in all_links:
        example = link.find('span', class_='text').get_text()
        example = example.strip('\r\n ')
        src_usage_examples.append(example)



    all_links = soup.find_all('div', class_='trg ltr')
    trg_usage_examples = []
    for link in all_links:
        example = link.find('span', class_='text').get_text()
        example = example.strip('\r\n ')
        trg_usage_examples.append(example)

    print(f"{trgt_language} Examples")

    combined_translations = zip(src_usage_examples, trg_usage_examples)
    for src, trg in combined_translations:
        print(src)
        print(trg)
        print()


welcoming_message()
src_language, trgt_language, word_to_translate = get_input()
web_content = make_request(src_language, trgt_language, word_to_translate)
find_word_translations(web_content)
find_word_usage_examples(web_content)




