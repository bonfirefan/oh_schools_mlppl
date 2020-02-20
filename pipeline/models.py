import numpy as np
from sklearn.linear_model import LogisticRegression

def logistic_regression(train_data, args=None):

    X_train = train_data.drop(columns=['graduated']).values
    y_train = train_data['graduated'].values

    l2_penalty = args[0]
    clf = LogisticRegression(random_state=0, C=l2_penalty, max_iter=500)
    clf.fit(X_train, y_train)

    print('Model coefs: ', clf.coef_)

    return clf

def random_guess(train_data, args=None):

    class RandomGuesser():
        def predict(self, X):
            return np.ones(len(X))

    clf = RandomGuesser()

    return clf
