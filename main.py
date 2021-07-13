from datetime import timedelta
from utils import collect_prices


def main():
    collect_prices(for_=timedelta(days=10), save_interval=timedelta(hours=1))


if __name__ == '__main__':
    main()
