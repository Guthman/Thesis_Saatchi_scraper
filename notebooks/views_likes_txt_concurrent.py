import requests as rq
import random
from time import sleep
import sqlite3
from bs4 import BeautifulSoup
import ujson
from concurrent.futures import ProcessPoolExecutor
import os


def get_random_waittime():
    waittime = random.weibullvariate(1, 5)/1.5
    return waittime


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.114 Safari/537.36',
    'Accept-Language': 'en,en-US;q=0,5',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8'
}

query_get = """select
       ART_ID,
       ARTWORK_URL
        from macro_dataset1
    where VIEWS is null and likes is null
    order by 1 asc
    ;"""


def get_views_likes(i):
    pid = os.getpid()
    with open(f"views_likes{pid}.txt", 'a') as f:
        url = i[1]
        art_id = i[0]
        page_html = rq.get(url, headers=headers)
        while page_html.status_code != 200 and page_html.status_code != 404:
            page_html = rq.get(url, headers=headers)
            print(page_html.status_code)
            sleep(get_random_waittime() * 8)

        if page_html.status_code == 404 or page_html.status_code > 499:
            print(page_html.status_code)
            views = -1
            likes = -1
        else:
            soup = BeautifulSoup(page_html.content, features='html.parser')
            j = soup.find('script', {'id': '__NEXT_DATA__'}).contents[0]
            j = ujson.loads(j)['props']['pageProps']['initialState']['page']['data']['artwork']
            views = j['views']
            likes = j['likes']
            f.write(str(art_id) + ',' + str(views) + ',' + str(likes) + '\n')


with sqlite3.connect(r'C:\Users\R\PycharmProjects\Thesis_Saatchi_scraper\datasets.db',
                     check_same_thread=False,
                     isolation_level=None) as con:
    cursor = con.execute(query_get)
    res = cursor.fetchall()


def main():
    with ProcessPoolExecutor(max_workers=6) as executor:
        executor.map(get_views_likes, res)


if __name__ == '__main__':
    main()
