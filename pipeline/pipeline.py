import argparse
from utils import download_data
from data_preparation import data_preparation, train_val_test_split

def main(args):

    # 1) Read data from database
    print('1. Downloading data...')
    data = download_data(user=args.user, password=args.password, tb_name=args.tb_name)

    # 2) Data preparation
    print('2. Data processing...')
    data = data_preparation(data, args = 1) # TODO: args can be the filter of which vars to use
    train_data, validation_data, test_data = train_val_test_split(data)

    # 3) Model
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parser')
    parser.add_argument("--user", required=True, type=str)
    parser.add_argument("--password", required=True, type=str)
    parser.add_argument("--tb_name", required=True, type=str)
    args = parser.parse_args()

    main(args)