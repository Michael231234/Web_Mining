import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score


def load_data():
    df = pd.read_csv('/Users/konglingtong/PycharmProjects/web_mining/new_data.csv').drop(['movieId', 'genres',
                                                                                         'timestamp', 'title'], axis=1)
    x = df.drop(['rating'], axis=1).values
    y = df['rating'].values

    return df, x, y


def decision_tree(x, y):
    depth = []
    for i in range(3, 20):
        clf = tree.DecisionTreeRegressor(max_depth=i)
        # Perform 7-fold cross validation
        scores = cross_val_score(estimator=clf, X=x, y=y, cv=10, n_jobs=4)
        depth.append((i, scores.mean()))
    print(depth)
    # clf = tree.DecisionTreeRegressor()
    # clf = clf.fit(x, y)
    # joblib.dump(clf, '/Users/konglingtong/PycharmProjects/web_mining/decision_tree.pkl')


def main():
    df, x, y = load_data()
    print(np.isnan(x))
    print(np.where(np.isnan(x)))
    new_x = np.nan_to_num(x)
    print()
    decision_tree(new_x, y)


main()  
