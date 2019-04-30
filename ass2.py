import requests
from bs4 import BeautifulSoup
import csv
import re


def get_top(url):
    r = requests.get(url=url)
    c = r.content
    soup = BeautifulSoup(c)
    ls = []
    rs = []
    ds = soup.select('table.wikitable>tbody>tr>td:nth-child(1)')
    for d in ds:
        ls.append(d.get_text().replace('[110]', '').replace('[ru]', '').replace('[74]', ''))
    sds = ['.example', '.invalid', '.local', '.localhost', '.onion', '.test']
    for sd in sds:
        if sd in ls:
            ls.remove(sd)
    for i in ls:
        obj = {}
        url = 'http://www.example%s' % (i)
        print(url)
        try:
            nr = requests.get(url=url)
            stc = nr.status_code
            obj['url'] = url
            obj['status_code'] = stc
        except requests.exceptions.ConnectionError:
            obj['url'] = url
            obj['status_code'] = 'err'
        except requests.exceptions.InvalidURL:
            obj['url'] = url
            obj['status_code'] = 'err'
        print(obj)
        rs.append(obj)

    return rs


def main():
    info = get_top('https://en.m.wikipedia.org/wiki/List_of_Internet_top-level_domains')
    headers = ['url', 'status_code']
    with open('ass2.csv', 'w') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(info)


main()