from sklearn import metrics

def metric_auc(clf, validation_data):
    # Validation data
    validation_data = validation_data.dropna()
    X = validation_data[['gpa_8','abs_8','int_8']].values
    y = validation_data['graduated'].values

    # Predictions
    y_hat = clf.predict(X)

    fpr, tpr, thresholds = metrics.roc_curve(y, y_hat, pos_label=1)
    auc = metrics.auc(fpr, tpr)

    print('AUC: ', auc)

    return auc



