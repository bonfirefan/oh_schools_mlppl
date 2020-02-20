from sklearn import metrics

def metric_auc(clf, test_data):
    # Test data
    X = test_data.drop(columns=['graduated']).values
    y = test_data['graduated'].values

    # Predictions
    y_hat = clf.predict(X)

    fpr, tpr, thresholds = metrics.roc_curve(y, y_hat, pos_label=1)
    auc = metrics.auc(fpr, tpr)

    print('AUC: ', auc)

    return auc

def accuracy(clf, test_data):
    # Test data
    X = test_data.drop(columns=['graduated']).values
    y = test_data['graduated'].values

    # Predictions
    y_hat = clf.predict(X)

    accuracy = (y_hat == y).mean()

    return accuracy

def confusion_matrix(clf, test_data):
    X = test_data.drop(columns=['graduated']).values
    y = test_data['graduated'].values

    # Predictions
    y_hat = clf.predict(X)
    confusion_matrix = pd.crosstab(y, y_hat, rownames=['Actual'], colnames=['Predicted'], normalize=True)
    print (confusion_matrix)
    return(confusion_matrix)
