import logging
import itertools

from gensim.utils import smart_open, simple_preprocess
from gensim.corpora.wikicorpus import _extract_pages, filter_wiki
from gensim.parsing.preprocessing import STOPWORDS

import gensim

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore


def head(stream, n=10):
    """Convenience fnc: return the first `n` elements of the stream, as plain list."""
    return list(itertools.islice(stream, n))


def tokenize(text):
    return [token for token in simple_preprocess(text) if token not in STOPWORDS]


def iter_wiki(dump_file):
    """Yield each article from the Wikipedia dump, as a `(title, tokens)` 2-tuple."""
    ignore_namespaces = 'Wikipedia Category File Portal Template MediaWiki User Help Book Draft'.split()
    for title, text, pageid in _extract_pages(smart_open(dump_file)):
        text = filter_wiki(text)
        tokens = tokenize(text)
        if any(title.startswith(ns + ':') for ns in ignore_namespaces):
            continue  # ignore short articles and various meta-articles
        yield title, tokens


stream = iter_wiki(
    '/Users/konglingtong/PycharmProjects/web_mining/enwiki-20170820-pages-articles.xml.bz2'
)
for title, tokens in itertools.islice(iter_wiki(
        '/Users/konglingtong/PycharmProjects/web_mining/test/'
        'enwiki-20190320-pages-articles-multistream1.xml-p10p30302.bz2'), 8):
    print(title, tokens[:10])  # print the article title and its first ten tokens

id2word = {0: u'word', 2: u'profit', 300: u'another_word'}
doc_stream = (tokens for _, tokens in iter_wiki(
    '/Users/konglingtong/PycharmProjects/web_mining/enwiki-20170820-pages-articles.xml.bz2'
))
id2word_wiki = gensim.corpora.Dictionary(doc_stream)
id2word_wiki.filter_extremes(no_below=20, no_above=0.1)


class WikiCorpus(object):
    def __init__(self, dump_file, dictionary, clip_docs=None):
        """
        Parse the first `clip_docs` Wikipedia documents from file `dump_file`.
        Yield each document in turn, as a list of tokens (unicode strings).

        """
        self.dump_file = dump_file
        self.dictionary = dictionary
        self.clip_docs = clip_docs

    def __iter__(self):
        self.titles = []
        for title, tokens in itertools.islice(iter_wiki(self.dump_file), self.clip_docs):
            self.titles.append(title)
            yield self.dictionary.doc2bow(tokens)

    def __len__(self):
        return self.clip_docs


def lda():
    # create a stream of bag-of-words vectors
    wiki_corpus = WikiCorpus(
        '/Users/konglingtong/PycharmProjects/web_mining/enwiki-20170820-pages-articles.xml.bz2'
        , id2word_wiki
    )
    vector = next(iter(wiki_corpus))
    print(vector)  # print the first vector in the stream
    gensim.corpora.MmCorpus.serialize('/Users/konglingtong/PycharmProjects/web_mining/wiki_bow.mm', wiki_corpus)
    wiki_corpus.dictionary.save_as_text('wiki_en_wordids2.txt')
    mm_corpus = gensim.corpora.MmCorpus('/Users/konglingtong/PycharmProjects/web_mining/wiki_bow.mm')
    print(mm_corpus)
    clipped_corpus = gensim.utils.ClippedCorpus(mm_corpus, 4000)
    lda_model = gensim.models.LdaModel(clipped_corpus, num_topics=20, id2word=id2word_wiki, chunksize=10000, passes=4)
    lda_model.save('/Users/konglingtong/PycharmProjects/web_mining/model/model.lda')

    return lda_model


def get_topic(path):
    lda = gensim.models.LdaModel.load('/Users/konglingtong/PycharmProjects/web_mining/model/model.lda')
    for i in range(3):
        p = 'wiki%s.txt' % str(i)
        f = open(path+p, 'r')
        data = f.read()
        dictionary = gensim.corpora.Dictionary.load_from_text('wiki_en_wordids2.txt')
        bow = dictionary.doc2bow(data.lower().split())
        doc_lda = lda[bow]
        print(doc_lda)



path = 'Users/konglingtong/PycharmProjects/web_mining/'
