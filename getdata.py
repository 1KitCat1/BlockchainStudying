import requests
import appdata


def get_current_data(from_sym='BTC', to_sym='USD', exchange=''):
    url = appdata.get_price_api_url

    parameters = {'fsym': from_sym,
                  'tsyms': to_sym}

    if exchange:
        print('exchange: ', exchange)
        parameters['e'] = exchange

    response = requests.get(url, params=parameters)
    data = response.json()

    return data
