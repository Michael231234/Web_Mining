import queue
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin
import re
from selenium import webdriver
import time


def is_absolute(url):
    """check weather url is absolute"""
    return bool(urlparse(url))


def sort(emails):
    """sort urls in file"""
    with open('/Users/konglingtong/PycharmProjects/web_mining/email.txt', 'w') as f:
        for email in emails:
            f.write(email)
            f.write('\n')


def main():
    q = queue.Queue()
    q.put('https://www.stevens.edu/')
    options = webdriver.ChromeOptions()
    options.add_argument('headerless')
    driver = webdriver.Chrome(executable_path='/Users/konglingtong/chromedriver', chrome_options=options)
    email_address = []
    ls = []
    for i in range(50):
        url = q.get()
        err_url = [
            '/account/register?r=https%3a%2f%2fgradadmissions.stevens.edu%2fapply%2f',
            '/account/login?r=https%3a%2f%2fgradadmissions.stevens.edu%2fapply%2f',
            '/account/register?r=https%3a%2f%2fgradadmissions.stevens.edu%2fapply%2f',
            'stevens.edu/ses',
            'Kurtis%20Watkins%20<kwatkins@stevens.edu>'
        ]
        if url not in err_url:
            print(url)
            driver.get(url)
            c = driver.page_source
            soup = BeautifulSoup(c, 'html.parser')
            links = soup.find_all('a')
            address = re.findall(r'\S+@stevens.edu+', soup.get_text())
            for a in address:
                if a not in email_address:
                    email_address.append(a)
                    print(a)
        # path = '/Users/konglingtong/%s' % (url.replace('https://', '').replace('http://', ''))
        # x = path[-1]
        # if x == '/':
        #     path = path
        # else:
        #     path = path + '/'
        # if not os.path.exists(path):
        #     os.makedirs(path)
            for link in links:
                u = link.get('href')
                if not is_absolute(u):
                    u = urljoin(url, u)
                if 'stevens.edu' in str(u):
                    if u not in ls:
                        ls.append(u)
                        q.put(u)
            time.sleep(1)

    print(ls)
    print(email_address)
    sort(email_address)
    exit()
    driver.close()


main()
