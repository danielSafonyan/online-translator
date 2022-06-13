import requests
from bs4 import BeautifulSoup

supported_languages = 'Arabic German English Spanish French ' \
                      'Hebrew Japanese Dutch Polish ' \
                      'Portuguese Romanian Russian Turkish'.lower().split()
dict_supported_languages = {str(idx + 1): language for idx, language in enumerate(supported_languages)}


def write_to_file(line):
    with open(f'{word_to_translate}.txt', 'a', encoding='utf-8') as file:
        file.write(line + '\n')


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

    if trgt_language == '0':
        return dict_supported_languages[src_language], '0', word_to_translate
    else:
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
    all_links = soup.select('a.translation.dict')
    word_translations = []
    for link in all_links:
        word = link.find('span', class_='display-term').get_text()
        word_translations.append(word)

    msg = f"{trgt_language.title()} Translations"
    print(msg)
    write_to_file(msg)
    for word in word_translations:
        print(word)
        write_to_file(word)
    print()
    write_to_file('')



def to_all_languages():
    for language in supported_languages:
        if language == src_language:
            continue
        web_content = make_request(src_language, language, word_to_translate)
        soup = BeautifulSoup(web_content, 'html.parser')
        all_links = soup.select('a.translation.dict')
        word = all_links[0].find('span', class_='display-term').get_text()
        msg = f"{language.title()} Translations:"
        print(msg)
        write_to_file(msg)
        print(word)
        write_to_file(word)
        print()
        write_to_file('')

        all_links = soup.find_all('div', class_='src ltr')
        example = all_links[0].find('span', class_='text').get_text()
        src_example = example.strip('\r\n ')
        all_links = soup.select('div.trg')
        example = all_links[0].find('span', class_='text').get_text()
        trgt_example = example.strip('\r\n ')

        msg = f"{language.title()} Example:"
        print(msg)
        write_to_file(msg)
        #
        print(src_example)
        write_to_file(src_example)
        print(trgt_example)
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
    print(msg)
    write_to_file(msg)

    combined_translations = zip(src_usage_examples, trg_usage_examples)
    for src, trg in combined_translations:
        print(src)
        write_to_file(src)

        print(trg)
        write_to_file(trg)

        print()
        write_to_file('')


welcoming_message()
src_language, trgt_language, word_to_translate = get_input()
if trgt_language == '0':
    to_all_languages()
else:
    web_content = make_request(src_language, trgt_language, word_to_translate)
    find_word_translations(web_content)
    find_word_usage_examples(web_content)




