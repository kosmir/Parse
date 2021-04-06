# импорт необходимых библиотек
import requests
from bs4 import BeautifulSoup
import csv
import string

def get_html(url):
    r = requests.get(url)
    return r.text

# получаем количество страниц, которое необходимо пропарсить
def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('ul', class_='page-numbers nav-pagination links text-center').find_all('a', class_='page-number')[1].get('href')
    total_pages = pages.split('/page/')[1].split('/')[0]
    return int(total_pages)

def write_csv(data):
    try:
        with open('sadovod4.csv', 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow((data['title'], data['url'], data['description']))
    # в случае ошибки записи смотрим на словарь, который записывает в csv
    except:
        print(data)

def get_page_data(html):
    soup = BeautifulSoup(html, "lxml")
    ads = soup.find('div', id='post-list').find_all('article')
    # для каждого объявления на странице получаю заголовок (title), адрес магазина в соцсетях (url), описание объявления (new_string)
    for ad in ads:
        try:
            #чистка заголовка от символов emodji
            old_title = ad.find('div', class_='entry-content').find('span', class_='post_title').text.strip()
            chars_avail = string.ascii_letters + string.digits + string.punctuation + string.whitespace \
                          + 'йцукенгшщзхъфывапролджэячсмитьбюёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ'
            new_title = ''.join([i for i in old_title if i in chars_avail])
        except:
            new_title = ''
        try:
            url = ad.find('div', class_='entry-content').find('span', class_='post_title').find('a').get('href')
        except:
            url = ''
            # чистка описания от символов emodji
        try:
            chars_avail = string.ascii_letters + string.digits + string.punctuation + string.whitespace \
                          + 'йцукенгшщзхъфывапролджэячсмитьбюёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ'
            old_string = ad.find('div', class_='article-inner').text.strip()
            new_string = ''.join([i for i in old_string if i in chars_avail])
            new_string = new_string.replace('\n', '')
        except:
            new_string = ''
        data = {'title': new_title,
                'url': url,
                'description': new_string}
        # вызов фунцкции для записи словаря в csv
        write_csv(data)

def main():
    url = 'https://sadovodbaza.ru/sumki-ryukzaki/'
    base_url = 'https://sadovodbaza.ru/sumki-ryukzaki'
    page_part = '/page/'
    total_pages = get_total_pages(get_html(url))
    for i in range(1, total_pages+1):
        url_gen = base_url + page_part + str(i)
        html = get_html(url_gen)
        get_page_data(html)

if __name__ == '__main__':
    main()