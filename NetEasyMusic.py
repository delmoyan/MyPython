import requests
import json
import os
import threading
from bs4 import BeautifulSoup

PLAY_LIST_FILE_PATH = "./wy/playlist.json"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/47.0.2526.80 Safari/537.36'
}


def save_playlist(page_count):
    url = 'https://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset={offset}'
    arr = []

    for x in range(page_count):
        print("抓取第{}页歌单:{}".format(x + 1, url.format(offset=x * 35)))
        response = requests.get(url.format(offset=x * 35), headers=HEADERS)
        html = BeautifulSoup(response.text, features="html.parser")
        play_list = html.select('#m-pl-container > li > div > a.msk')
        for pl in play_list:
            arr.append({"href": pl.get('href'), "name": pl.get('title')})

    with open(PLAY_LIST_FILE_PATH, 'wb') as f:
        f.write(bytes(str(json.dumps(arr, ensure_ascii=False)), 'utf-8'))


def init_songs():
    arr = []
    with open(PLAY_LIST_FILE_PATH, 'r', encoding='UTF-8') as f:
        play_list = json.load(f)
        threads = []
        while len(play_list) > 0:
            for thread in threads:
                if not thread.is_alive():
                    threads.remove(thread)

            while len(threads) < 50 and len(play_list) > 0:  # 最多50个线程
                pl = play_list.pop(0)
                thread = threading.Thread(target=get_playlist_songs, args=(pl, arr))
                thread.setDaemon(True)
                thread.start()
                print('{}正在抓取歌单歌曲列表，还剩{}个歌单。'.format(threading.current_thread().name, len(play_list)))
                threads.append(thread)

    if os.access(PLAY_LIST_FILE_PATH, os.W_OK):
        with open(PLAY_LIST_FILE_PATH, 'wb') as f:
            f.write(bytes(str(json.dumps(arr, ensure_ascii=False)), 'utf-8'))


def get_playlist_songs(playlist, all_array):
    tag_arr = []
    song_arr = []

    url = "https://music.163.com" + playlist['href']
    response = requests.get(url, headers=HEADERS)

    html = BeautifulSoup(response.text, features="html.parser")
    tag_list = html.select(".tags.f-cb > .u-tag")  # 获取歌单标签
    song_list = html.select("#song-list-pre-cache > ul > li > a")  # 获取歌单歌曲列表

    for tag in tag_list:
        tag_arr.append(tag.text)
    for song in song_list:
        song_arr.append({
            "href": song.get("href"),
            "name": song.text
        })

    playlist['tags'] = tag_arr
    playlist['songs'] = song_arr
    all_array.append(playlist)


if __name__ == '__main__':
    # save_playlist(50)
    init_songs()
