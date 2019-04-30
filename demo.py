import logging
import gensim

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore


def get_topic(path):
    lda = gensim.models.LdaModel.load('/Users/konglingtong/PycharmProjects/web_mining/model/model.lda')
    lda.print_topics()
    print(lda)
    for i in range(3):
        p = 'wiki%s.txt' % str(i)
        print(p)
        f = open(path+p, 'r')
        data = f.read()
        dictionary = gensim.corpora.Dictionary.load_from_text('wiki_en_wordids2.txt')
        bow = dictionary.doc2bow(data.lower().split())
        print(bow)
        doc_lda = lda[bow]
        print(doc_lda)

path = '/Users/konglingtong/PycharmProjects/web_mining/'
get_topic(path)
