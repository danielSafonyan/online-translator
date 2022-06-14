import requests
from bs4 import BeautifulSoup
import argparse

supported_languages = 'Arabic German English Spanish French ' \
                      'Hebrew Japanese Dutch Polish ' \
                      'Portuguese Romanian Russian Turkish'.lower().split()
dict_supported_languages = {str(idx + 1): language for idx, language in enumerate(supported_languages)}


def write_to_file(line):
    with open(f'{word_to_translate}.txt', 'a', encoding='utf-8') as file:
        file.write(line + '\n')


def print_file():
    with open(f'{word_to_translate}.txt', 'r', encoding='utf-8') as file:
        print(file.read())


def get_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('src_language')
    parser.add_argument('trgt_language')
    parser.add_argument('word_to_translate')

    args = parser.parse_args()

    src_language = args.src_language
    trgt_language = args.trgt_language
    word_to_translate = args.word_to_translate

    if trgt_language == 'all':
        return src_language, 'all', word_to_translate
    else:
        return src_language, trgt_language, word_to_translate


def make_request(src_language, trgt_language, word_to_translate):
    url = f'https://context.reverso.net/translation/{src_language}-{trgt_language}/{word_to_translate}'
    while True:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            break
    return r.content


def find_word_translations(content):
    soup = BeautifulSoup(content, 'html.parser')
    all_links = soup.select('a.translation.dict')
    word_translations = []
    for link in all_links:
        word = link.find('span', class_='display-term').get_text()
        word_translations.append(word)

    msg = f"{trgt_language.title()} Translations"
    write_to_file(msg)
    for word in word_translations:
        write_to_file(word)
    write_to_file('')



def to_all_languages():
    for language in supported_languages:
        if language == src_language:
            continue
        web_content = make_request(src_language, language, word_to_translate)
        soup = BeautifulSoup(web_content, 'html.parser')
        all_links = soup.select('a.translation.dict')
        word = all_links[0].get_text()
        msg = f"{language.title()} Translations:"
        write_to_file(msg)
        write_to_file(word)
        write_to_file('')

        all_links = soup.find_all('div', class_='src ltr')
        example = all_links[0].find('span', class_='text').get_text()
        src_example = example.strip('\r\n ')
        all_links = soup.select('div.trg')
        example = all_links[0].find('span', class_='text').get_text()
        trgt_example = example.strip('\r\n ')

        msg = f"{language.title()} Example:"
        write_to_file(msg)
        #
        write_to_file(src_example)
        write_to_file(trgt_example)
        write_to_file('')


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

    msg = f"{trgt_language.title()} Examples"
    write_to_file(msg)

    combined_translations = zip(src_usage_examples, trg_usage_examples)
    for src, trg in combined_translations:
        write_to_file(src)

        write_to_file(trg)

        write_to_file('')


# welcoming_message()
src_language, trgt_language, word_to_translate = get_input()
if trgt_language == 'all':
    to_all_languages()
else:
    web_content = make_request(src_language, trgt_language, word_to_translate)
    find_word_translations(web_content)
    find_word_usage_examples(web_content)
print_file()




