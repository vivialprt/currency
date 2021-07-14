import requests


API_VERSION = 'v1'
BASE_URL = 'https://api-adapter.backend.currency.com/api/{}/'.format(
    API_VERSION
)
SERVER_TIME_ENDPOINT = BASE_URL + 'time'
PRICE_CHANGE_24H_ENDPOINT = BASE_URL + 'ticker/24hr'


def get_server_time():
    r = requests.get(SERVER_TIME_ENDPOINT, timeout=30)
    return r.json()


def get_24h_price_change(symbol=None):
    r = requests.get(
        PRICE_CHANGE_24H_ENDPOINT,
        params={'symbol': symbol} if symbol else {},
        timeout=30
    )
    return r.json()
