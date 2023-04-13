import os
import requests
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv, find_dotenv


def shorten_link(token, link):
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {
        "Authorization": f"Bearer {token}"
    }
    body = {
        "long_url": link
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    bitlink = response.json()['link']
    return bitlink


def count_clicks(token, link):
    bitlink_parse = urlparse(link)
    bitlink = bitlink_parse._replace(scheme='').geturl()
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(token, link):
    bitlink_parse = urlparse(link)
    bitlink = bitlink_parse._replace(scheme='').geturl()
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    result = response.ok
    return result


def main():
    load_dotenv(find_dotenv())
    parser = argparse.ArgumentParser(
        description='Описание что делает программа'
    )
    parser.add_argument('user_link', help='Ссылка на страницу')
    args = parser.parse_args()
    token = os.environ['BITLY_GENERIC_ACCESS_TOKEN']

    try:
        if not is_bitlink(token, args.user_link):
            bitlink = shorten_link(token, args.user_link)
            print('Битлинк', bitlink)
        else:
            clicks_count = count_clicks(token, args.user_link)
            print('Всего кликов', clicks_count)
    except requests.exceptions.HTTPError:
        print('Invalid input')


if __name__ == '__main__':
    main()
