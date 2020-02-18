from sklearn.linear_model import LogisticRegression

def logistic_regression(train_data, args=None):

    train_data = train_data.dropna()
    X_train = train_data[['gpa_8','abs_8','int_8']].values
    y_train = train_data['graduated'].values

    clf = LogisticRegression(random_state=0)
    clf.fit(X_train,y_train)

    print('Model coefs: ', clf.coef_)

    return clf