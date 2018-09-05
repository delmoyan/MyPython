import requests
from bs4 import BeautifulSoup


def save_playlist():
    file_path = './wy/playlist/{page}.json'
    url = 'https://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset={offset}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    for x in range(1):
        response = requests.get(url.format(offset=x * 35), headers=headers)
        print(response.url)
        html = BeautifulSoup(response.text)
        play_list = html.select('#m-pl-container > li')
        for pl in play_list:
            print(str(pl.select('a.msk')))

        # with open(file_path.format(page='page_' + str(x + 1)), 'wb') as f:
        #     f.write(response.content)


if __name__ == '__main__':
    save_playlist()
