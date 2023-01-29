from pyuseragents import random as random_u
import cloudscraper
from bs4 import BeautifulSoup
from cprint import *


class CheckNetwork:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()

    def network_search(self, wallet):
        test_network = ['ropsten', 'goerli', 'mumbai', 'moonbase.moonscan.io', 'test']
        headers = {
            'authority': 'blockscan.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                      'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'ru,en;q=0.9,ru-BY;q=0.8,ru-RU;q=0.7,en-US;q=0.6',
            'cache-control': 'max-age=0',
            'cookie': '_ga=GA1.2.473459829.1671458361; _gid=GA1.2.1112637907.1674913586',
            'referer': 'https://bscscan.com/',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': random_u(),
        }
        self.scraper.headers.update(headers)
        response = self.scraper.get(
            f'https://blockscan.com/address/{wallet}',
        )
        soup = BeautifulSoup(response.text, 'lxml')
        url_network = []
        for i in soup.find_all('a'):
            text = i.get('href')
            flag = True
            if wallet in text and 'https' in text and 'test' not in text:
                for network in test_network:
                    if network in text:
                        flag = False
                if flag:
                    url_network.append(text)
        return url_network

    def search_token(self, url: list[str], wallet):
        cprint.warn('Wallet: ' + wallet)
        for url_ in url:
            url_ = url_
            auth = url_.split('/')[2]
            headers = {
                'authority': auth,
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                          'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-language': 'ru,en;q=0.9,ru-BY;q=0.8,ru-RU;q=0.7,en-US;q=0.6',
                'cache-control': 'max-age=0',
                'referer': 'https://blockscan.com/',
                'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'cross-site',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': random_u(),
            }

            response = self.scraper.get(
                url_,
                headers=headers,
            )
            soup = BeautifulSoup(response.text, 'lxml')
            #######################################################################
            token_network = str(soup.find('div', class_='col-md-8')).replace('<div class="col-md-8">', '').\
                replace('</b>', '').replace('<b>', '').replace('</div>', '')
            ########################################################################
            tokens_list = []
            NFT = []
            for tokens in soup.find_all('li'):
                text = str(tokens.select('span'))
                if 'text-monospace' in text:
                    name = text.split('hash-tag--md text-truncate text-monospace">')[1].split('</span>')[0]
                    NFT.append(name)
                elif 'text-truncate">' in text:
                    name = text.split('hash-tag--md text-truncate">')[1].split('</span>')[0]
                    tokens_list.append(name)
            cprint.ok(token_network)
            cprint.info('Tokens: ' + '; '.join(tokens_list))
            cprint.info('NFT: ' + '; '.join(NFT))
            cprint.info('URL: ' + url_)
            print('')

    @staticmethod
    def collecting_wallets():
        with open('wallet.txt', 'r') as wallet:
            return wallet.read().splitlines()


def main():
    network = CheckNetwork()
    list_wallets = network.collecting_wallets()
    print('\033[35m*' * 100)
    print(f'\033[35mUploaded \033[36m{len(list_wallets)}\033[35m addresses')
    print('\033[35m*' * 100)
    print('')
    for wallet in list_wallets:
        url_network = network.network_search(wallet)
        network.search_token(url_network, wallet)


if __name__ == '__main__':
    main()
