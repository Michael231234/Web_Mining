import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from sklearn.svm import SVC


def process_data():
    rate_df = pd.read_csv('/Users/konglingtong/PycharmProjects/web_mining/ml-latest-small/ratings.csv')
    genome_scores = pd.read_csv('/Users/konglingtong/PycharmProjects/web_mining/ml-20m/genome-scores.csv')
    # genome_tags = pd.read_csv('/Users/konglingtong/PycharmProjects/web_mining/ml-20m/genome-tags.csv')
    movies = pd.read_csv('/Users/konglingtong/PycharmProjects/web_mining/ml-latest-small/movies.csv')

    new_genome_scores = genome_scores.pivot_table(index='movieId', columns='tagId', values='relevance')
    c = [
        'Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy', 'Romance', 'Drama', 'Action', 'Crime', 'Thriller',
        'Horror', 'Mystery', 'Sci-Fi', 'War', 'Musical', 'Documentary', 'IMAX', 'Western', 'Film-Noir'
    ]
    # print(new_genome_scores)
    # print(movies['genres'].str.split('|'))
    movies['genres'] = movies['genres'].str.split('|')
    new_movies = pd.concat([movies, pd.DataFrame(columns=c)], sort=False)
    # print(new_movies)
    for i, r in new_movies.iterrows():
        for col in c:
            genres = new_movies.loc[i, 'genres']
            if col in genres:
                new_movies.loc[i, col] = 1
            else:
                new_movies.loc[i, col] = 0
    # print(new_movies)
    # new_movies.to_csv("new_movies.csv")
    new_rate = pd.merge(rate_df, new_movies, how='inner')
    new_data = pd.concat([new_rate, new_genome_scores])
    new_data['userId'] = new_data['userId'].fillna(-1)
    new_df = new_data[new_data['userId'] != -1]
    for c in new_df.columns:
        print(c)

    # new_df.to_csv("new_data.csv")
    # print(new_rate[new_rate['userId'] == 1].sort_values('movieId', ascending=True))
    # print(new_rate.sort_values('userId', ascending=True))

    return new_df


def load_data():
    df = pd.read_csv('/Users/konglingtong/PycharmProjects/web_mining/new_data.csv').drop(['movieId', 'genres',
                                                                                         'timestamp', 'title'], axis=1)
    x = df.drop(['rating'], axis=1).values
    y = df['rating'].values

    return df, x, y


def eclud_sim(ina, inb):
    return 1.0/(1.0+np.linalg.norm(ina-inb))


def pears_sim(ina, inb):
    if len(ina) < 3:
        return 1.0
    return 0.5+0.5*np.corrcoef(ina, inb)[0][1]


def cos_sim(ina, inb):
    num = float(ina.T*inb)
    denom = np.linalg.norm(ina)*np.linalg.norm(inb)
    return 0.5+0.5*(num/denom)


def sigma_pct(sigma, percentage):
    sigma2 = sigma**2
    sumsigma2 = sum(sigma2)
    sumsigma3 = 0
    k = 0
    for i in sigma:
        sumsigma3 += i**2
        k += 1
        if sumsigma3 >= sumsigma2*percentage:
            return k


def svd(datamat, percentage, ratings, item):
    n = np.shape(datamat)[1]
    sim_total = 0.0
    rat_sim_total = 0.0
    u, sigma, vt = np.linalg.svd(datamat)
    k = sigma_pct(sigma, percentage)
    sigma_k = np.mat(np.eye(k)*sigma[:k])
    xformed_items = datamat.T*u[:, :k]*sigma_k.I
    for r in range(n):
        rating = ratings[n]
        similarity = cos_sim(xformed_items[item, :].T, xformed_items[r, :].T)
        sim_total += similarity
        rat_sim_total += similarity*rating
    if sim_total == 0:
        print(0)
        return 0
    else:
        print(rat_sim_total/sim_total)
        return rat_sim_total/sim_total


def recommed(datamat, user, ratings, N, est_method=svd, percentage=0.9):
    print(datamat[user, :])
    unrated = np.nonzero(datamat[user, :] == 0)
    if len(unrated) == 0:
        return 0
    itemscores = []
    for item in unrated:
        estimated_score = est_method(datamat, percentage, ratings, item)
        itemscores.append((item, estimated_score))
    itemscores = np.sort(itemscores, key=lambda x:x[1], reverse=True)
    return itemscores[:N]


if __name__ == "__main__":
    data, x, y = load_data()
    recommed(x, 1, y, N=3, percentage=0.8)
    # process_data()
