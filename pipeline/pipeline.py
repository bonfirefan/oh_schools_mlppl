import argparse
from utils import download_data, upload_result
from data_preparation import data_preparation, train_val_test_split
from models import logistic_regression
from evaluation import metric_auc

model_dict = {'logistic_reg':logistic_regression}

def main(args):

    # 1) Read data from database
    print(20*'=')
    print('1. Downloading data...')
    data = download_data(user=args.user, password=args.password, tb_name=args.tb_name)

    # 2) Data preparation
    print(20*'=')
    print('2. Data processing...')
    data = data_preparation(data, args = 1) # TODO: args can be the filter of which vars to use
    train_data, validation_data, test_data = train_val_test_split(data)

    # 3) Model
    print(20*'=')
    print('Training model...')
    model = model_dict[args.model]
    clf = model(train_data, args=None)

    # 4) Compute metric in validation set
    print(20*'=')
    print('Evaluation model in validation set...')
    auc, accuracy = metric_auc(clf, validation_data)

    # 5) Upload result to postgres
    print(20*'=')
    print('Uploading result to database...')
    upload_result(args.model_short_name, auc, args.user, args.password)
    print('FINISHED!!!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parser')
    parser.add_argument("--user", required=True, type=str)
    parser.add_argument("--password", required=True, type=str)
    parser.add_argument("--tb_name", required=True, type=str)
    parser.add_argument("--model", required=True, type=str)
    parser.add_argument("--model_short_name", required=True, type=str)

    args = parser.parse_args()

    main(args)