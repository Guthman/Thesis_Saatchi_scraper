import requests as rq
from concurrent.futures import ProcessPoolExecutor
import random
from time import sleep
import sqlite3
from bs4 import BeautifulSoup
import ujson


def get_random_waittime():
    waittime = random.weibullvariate(1, 5)/1.5
    return waittime


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.114 Safari/537.36',
    'Accept-Language': 'en,en-US;q=0,5',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8'
}

con = sqlite3.connect(r'C:\Users\R\PycharmProjects\Thesis_Saatchi_scraper\datasets.db',
                      check_same_thread=False,
                      isolation_level=None)

query_get = """select
       ART_ID,
       ARTWORK_URL
        from macro_dataset1
    where VIEWS is null and likes is null
    order by 1 asc
    ;"""

query_put = "update macro_dataset1 set LIKES = ?, VIEWS = ? where ART_ID = ?;"

cursor = con.execute(query_get)
res = cursor.fetchall()
print('Fetched list')


def get_views_likes(i):
    url = i[1]
    art_id = i[0]
    page_html = rq.get(url, headers=headers)
    while page_html.status_code != 200 and page_html.status_code != 404:
        page_html = rq.get(url, headers=headers)
        print(page_html.status_code)
        sleep(get_random_waittime() * 8)

    if page_html.status_code == 404 or page_html.status_code > 499:
        print(page_html.status_code)
        con.execute(query_put, (-1, -1, art_id))
    else:
        soup = BeautifulSoup(page_html.content, features='html.parser')
        j = soup.find('script', {'id': '__NEXT_DATA__'}).contents[0]
        j = ujson.loads(j)
        views = j['props']['pageProps']['initialState']['page']['data']['artwork']['views']
        likes = j['props']['pageProps']['initialState']['page']['data']['artwork']['likes']
        con.execute(query_put, (likes, views, art_id))
        sleep(get_random_waittime())


def main():
    with ProcessPoolExecutor(max_workers=4) as executor:
        executor.map(get_views_likes, res)


if __name__ == '__main__':
    main()
