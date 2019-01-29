import requests


def post_response(url):
    r = requests.post(url=url)
    c = r.text
    h = r.headers
    s = r.status_code

    print('content', c)
    print('------------------')
    print('headers', h)
    print('------------------')
    print('status_code', s)
    print('------------------')


def get_response(url):
    r = requests.get(url=url)
    c = r.text
    h = r.headers
    s = r.status_code

    print('content', c)
    print('------------------')
    print('headers', h)
    print('------------------')
    print('status_code', s)
    print('------------------')

google_url = 'https://www.google.com/search?newwindow=1&source=hp&ei=xxZLXNCCAuii_QaProAg&q=Tim+Berners-Lee&btnK=Google+Search&oq=Tim+Berners-Lee&gs_l=psy-ab.3..35i39j0l9.1184.1184..1393...1.0..0.121.201.1j1......0....2j1..gws-wiz.....6._QHWuI0aBs4'
get_response(google_url)
get_url = 'https://itbilu.com'
post_response(get_url)
fake_url = 'https://www.pixiv.net/12132313/'
get_response(fake_url)
get_response(get_url)