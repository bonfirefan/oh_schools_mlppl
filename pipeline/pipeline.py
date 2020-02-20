import argparse
import yaml
import time

from utils import download_data, upload_result
from data_preparation import data_preparation, train_val_test_split
from models import logistic_regression, random_guess
from evaluation import metric_auc, accuracy

model_dict = {'logistic_reg': logistic_regression,
              'random_guess': random_guess}

metric_dict = {'AUC':metric_auc}

def main(args, config):
    start_time = time.time()
    # 1) Read data from database
    print(20*'=')
    print('1. Downloading data...')
    data = download_data(user=args.user, password=args.password,tb_name='sketch.train_data_2')
    oh = download_data(user=args.user, password=args.password,tb_name='sketch.ode_school')
    # 2) Data preparation
    print(20*'=')
    print('2. Data processing...')
    data = data_preparation(data, oh) # TODO: args can be the filter of which vars to use
    train_data, test_data = train_val_test_split(data, config['min_train_cohort'], config['min_test_cohort'])

    # 3) Model
    print(20*'=')
    print('3. Training model...')
    model = model_dict[config['model']]
    clf = model(train_data, args=config['hyperparameters'])

    # 4) Compute metric in validation set
    print(20*'=')
    print('4. Evaluation model in validation set...')
    metric = metric_dict[config['metric']](clf, test_data)
    print('{}: {}', config['metric'], metric)

    # We print test and train accuracy
    train_accuracy = accuracy(clf, train_data)
    print('Train accuracy: ', train_accuracy)
    test_accuracy = accuracy(clf, test_data)
    print('Test accuracy: ', test_accuracy)

    # 5) Upload result to postgres
    print(20*'=')
    print('5. Uploading result to database...')
    upload_result(config['model_name'], config['metric'], metric, args.user, args.password)

    print(20*'=')
    print('Finished in {} seconds'.format(time.time()-start_time))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parser')
    parser.add_argument("--user", required=True, type=str)
    parser.add_argument("--password", required=True, type=str)
    parser.add_argument("--config_path", required=True, type=str)

    args = parser.parse_args()

    with open(args.config_path, 'r') as stream:
        config = yaml.safe_load(stream)

    main(args, config)
