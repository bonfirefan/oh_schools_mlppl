import argparse
from utils import download_data


def main(args):

    # 1) Read data from database
    print('1. Downloading data...')
    data = download_data(user=args.user, password=args.password, tb_name=args.tb_name)

    print(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parser')
    parser.add_argument("--user", required=True, type=str)
    parser.add_argument("--password", required=True, type=str)
    parser.add_argument("--tb_name", required=True, type=str)
    args = parser.parse_args()

    main(args)