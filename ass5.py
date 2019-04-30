import requests
from bs4 import BeautifulSoup
import re
import spacy
import math
import numpy as np
from scipy import stats


def get_books():
    """get top 100 books from www.gutenberg.org"""
    r = requests.get('https://www.gutenberg.org/browse/scores/top')
    c = r.content
    soup = BeautifulSoup(c)
    links = soup.select('.body ol:nth-of-type(1) li a[href*="ebooks"]')
    ebook_links = []
    ps = []
    for link in links:
        print(link.get('href'))
        book_link = 'https://www.gutenberg.org/%s' % link.get('href')
        ebook_links.append(book_link)
        br = requests.get(book_link)
        bc = br.content
        soup = BeautifulSoup(bc)
        txt_link = soup.select('a[href*=".txt"]')
        if len(txt_link) != 0:
            tl = 'https:%s' % txt_link[0].get('href')
        else:
            tl = 'https:%s' % soup.select('a[href*=".tex"]')[0].get('href')
        text = requests.get(tl)
        book = text.text
        num = re.findall(r'\d+', link.get('href'))[0]
        path = '/Users/konglingtong/PycharmProjects/web_mining/books/%s' % (num + '.txt')
        ps.append(path)
        f = open(path, 'w')
        f.write(book)
        f.close()

    print(ps)
    f = open('path.txt', 'w')
    f.write(ps)
    f.close()

    return ps


def nlp(path):
    t = 0
    v = 0
    names = []
    sentences = []
    ns = 0
    pl = spacy.load('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/spacy/data/en/'
                    'en_core_web_sm-2.0.0')
    for p in path:
        tokens = []
        verbs = []
        file = open(p)
        text = file.read()
        if len(text) > 10**6:
            n = math.ceil(len(text)/10**6)
            for i in range(n):
                x1 = (10**6)*i
                x2 = (10**6)*(i+1)
                if x2 > len(text):
                    x2 = len(text)
                new_text = text[x1: x2]
                doc = pl(new_text)
                for token in doc:
                    if token.pos_ == 'VERB':
                        v += 1
                        verbs.append(token)
                    if token.tag_ == 'NNP':
                        names.append(token)
                    tokens.append(token)
                for sent in doc.sents:
                    sentences.append(sent)
                    if len(sent) > 10:
                        ns += 1
        else:
            doc = pl(text)
            for token in doc:
                if token.pos_ == 'VERB':
                    v += 1
                    verbs.append(token)
                if token.tag_ == 'NNP':
                    names.append(token)
                tokens.append(token)
            for sent in doc.sents:
                sentences.append(sent)
                if len(sent) > 10:
                    ns += 1
        t += len(tokens)
        n = re.findall(r'\d+\.txt', p)
        print('tokens in file %s is:' % n[0], len(tokens))
        print('verbs in file %s is:' % n[0], len(verbs))
    txt = str(sentences[14])
    wv = pl(txt)
    print('vector:', wv[0].vector)
    n_names = np.array(names)
    print('most frequent named:', stats.mode(n_names)[0][0])
    print('token in all document:', t)
    print('verb in all document:', v)
    print('sentences in the document:', len(sentences))
    print('sentences at least 10 words', ns)


book_path = get_books()
nlp(book_path)
