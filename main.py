from bs4 import BeautifulSoup
import requests
import time


def parse(html_data):
    soup = BeautifulSoup(html_data, 'lxml')

    values = soup.findAll('div', attrs={'itemprop': 'review'})

    for value in values:
        author_tag = value.find('meta', attrs={'itemprop': 'author'})
        print(author_tag['content'])

        reviewRating_tag = value.find('div', attrs={'itemprop': 'reviewRating'})
        print(reviewRating_tag.meta['content'])

        description_tag = value.find('meta', attrs={'itemprop': 'description'})
        print(description_tag['content'])


# file = open('yandex_market_page.html', 'r', encoding='utf-8')
# data = file.read()
# file.close()


def get_next_page_url(html_data):
    soup = BeautifulSoup(html_data, 'lxml')
    tag = soup.find('a', attrs={'aria-label': 'Следующая страница'})

    if tag is None:
        return None
    else:
        return 'https://market.yandex.ua/' + tag['href']


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'market.yandex.ua',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
}

url = 'https://market.yandex.ua/product--smartfon-apple-iphone-12-128gb/722974019/reviews?track=tabs&onstock=1'

while True:
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    data = response.text
    parse(data)

    time.sleep(10)
    url = get_next_page_url(data)

    if url is None:
        break
