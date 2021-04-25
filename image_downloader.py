import requests as rq
import random
import ujson
from tqdm.auto import tqdm
from time import sleep


def get_random_waittime():
    waittime = random.weibullvariate(1, 5)/1.5
    return waittime


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.114 Safari/537.36',
    'Accept-Language': 'en,en-US;q=0,5',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8'
}

url = 'https://mnr6yzqr22jgywm-adw2.adb.eu-frankfurt-1.oraclecloudapps.com/ords/thesisproject/sp/g'

while True:
    response = rq.get(url)
    urls = ujson.loads(response.content)['items']

    for img in tqdm(urls[:2]):
        id_ = str(img['id'])
        art_id = str(img['art_id'])
        image_url = img['image_url']
        artwork_id = str(img['artwork_id'])
        artist_id = str(img['artist_id'])
        filename = str(id_ + '_' +
                       art_id + '_' +
                       artwork_id + '_' +
                       artist_id + '_' +
                       image_url.split('/')[-1])
        missing = '-1'

        # mark as doing
        rq.put(f'https://mnr6yzqr22jgywm-adw2.adb.eu-frankfurt-1.oraclecloudapps.com/ords/thesisproject/sp/doing/{id_}')
        res = rq.get(image_url, headers=headers)
        http_status_code = res.status_code

        # download images
        open('./images/' + filename, 'wb').write(res.content)
        insert_url = f'https://mnr6yzqr22jgywm-adw2.adb.' \
                     f'eu-frankfurt-1.oraclecloudapps.com/ords/thesisproject/sp/img_done/' \
                     f'{id_ or missing}/' \
                     f'{art_id or missing}/' \
                     f'{artwork_id or missing}/' \
                     f'{artist_id or missing}/' \
                     f'{filename or missing}/' \
                     f'{http_status_code}'
        rq.post(insert_url)

    # mark as done
    rq.put(f'https://mnr6yzqr22jgywm-adw2.adb.eu-frankfurt-1.oraclecloudapps.com/ords/thesisproject/sp/{id_}')
    sleep(get_random_waittime())
