import requests
import re
from bs4 import BeautifulSoup

URLS = [
    "https://www.anekdot.ru/release/aphorism/year/2021/",
    "https://www.anekdot.ru/release/aphorism/year/2020/",
    "https://www.anekdot.ru/release/aphorism/year/2019/",
    "https://www.anekdot.ru/release/aphorism/year/2018/",
    "https://www.anekdot.ru/release/aphorism/year/2017/",
    "https://www.anekdot.ru/release/aphorism/year/2016/",
    "https://www.anekdot.ru/release/aphorism/year/2015/",
    "https://www.anekdot.ru/release/aphorism/year/2014/",
    "https://www.anekdot.ru/release/aphorism/year/2013/",
    "https://www.anekdot.ru/release/aphorism/year/2012/",
    "https://www.anekdot.ru/release/aphorism/year/2011/",
    "https://www.anekdot.ru/release/aphorism/year/2010/",
    "https://www.anekdot.ru/release/aphorism/year/2009/",
    "https://www.anekdot.ru/release/aphorism/year/2008/",
    "https://www.anekdot.ru/release/aphorism/year/2007/",
    "https://www.anekdot.ru/release/aphorism/year/2006/",
    "https://www.anekdot.ru/release/aphorism/year/2005/",
    "https://www.anekdot.ru/release/aphorism/year/2004/",
    "https://www.anekdot.ru/release/aphorism/year/2003/",
    "https://www.anekdot.ru/release/aphorism/year/2002/",
    "https://www.anekdot.ru/release/aphorism/year/2001/",
    "https://www.anekdot.ru/release/aphorism/year/2000/"
]

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0', 'accept': '*/*'}


def get_html(url, params = None):
    result = requests.get(url, headers=HEADERS, params=params)
    return result

def get_pages_count(html, url):
    count = 1
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('div', class_='pageslist')
    pages = pagination.find_all('a')
    if pages[-1].get_text() == 'след. →':
        count = get_pages_count(get_html(url+f'{int(pages[-2].get_text())}/').text, url)
        return count
    else:
        return int(pages[-1].get_text())+1

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='topicbox')

    anekdots = []
    for item in items:
        text = item.find('div', class_='text')
        if text != None:
            anekdots.append(text.get_text())
    return anekdots


def parse():
    anekdots = []
    for url in URLS:
        html = get_html(url)
        if html.status_code == 200:
            page_count = get_pages_count(html.text, url)
            print(f"\tURL {url}:")
            for page in range(1, page_count+1):
                print(f"\t\tParse page: {page} / {page_count}")
                html = get_html(url+str(page)+'/')
                anekdots.extend(get_content(html.text))
        else:
            print(f"Can't get html: {url}")

    return anekdots


anekdots = parse()
f = open('input.txt', 'a', encoding='utf-8')
for anekdot in anekdots:
    anekdot = re.sub(r'https?\S+', '', anekdot, flags=re.MULTILINE)
    anekdot = re.sub(r'www\S+', '', anekdot, flags=re.MULTILINE)
    anekdot = re.sub(r'\(c\) ?\S*', '', anekdot, flags=re.MULTILINE)
    anekdot = re.sub(r'\(C\) ?\S*', '', anekdot, flags=re.MULTILINE)
    anekdot = re.sub(r'\(c\) ?\S*', '', anekdot, flags=re.MULTILINE) # русские с
    anekdot = re.sub(r'\(C\) ?\S*', '', anekdot, flags=re.MULTILINE)  # русские с

    f.write(anekdot+'\n')