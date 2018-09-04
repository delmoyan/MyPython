import itchat
import codecs
import json
import os
import re
from collections import Counter
from pyecharts import Pie
from pyecharts import Bar
from pyecharts import Grid
from pyecharts import WordCloud
import jieba.analyse


# save the friends json data to file system
def save_data(friends):
    out_file_path = './json_data/friends.json'
    if not os.access(out_file_path, os.F_OK):
        with codecs.open(out_file_path, 'w', encoding='UTF-8') as file:
            print('create file in "/json_data/friends.json".')
            file.write(json.dumps(friends, ensure_ascii=False))


# download friends head image
def download_images(friends):
    img_dir = './head_images/'
    if not os.access(img_dir, os.F_OK) or not os.listdir(img_dir):
        print('create file in "/head_images/".')
    for friend in friends:
        img = itchat.get_head_img(userName=friend['UserName'])
        with open(img_dir + friend['UserName'] + '.jpg', 'wb') as file:
            file.write(img)


def dict2list(_dict):
    name_list = []
    num_list = []
    for key, value in _dict.items():
        name_list.append(key)
        num_list.append(value)
    return name_list, num_list


def get_pie(name, name_list, num_list):
    total = sum(num_list)
    subtitle = "共有:%d个好友：" % total
    pie = Pie(name, page_title=name, title_text_size=30, title_pos='center', subtitle=subtitle, subtitle_text_size=25,
              width=800, height=800)
    pie.add("", name_list, num_list, is_label_show=True, center=[50, 45], radius=[0, 50], legend_pos='left',
            legend_orient='vertical', label_text_size=20)
    output_file = './chart/%s.html' % name
    pie.render(output_file)


def get_bar(name, name_list, num_list):
    sub_title = '好友省份来源'
    bar = Bar(name, page_title=name, title_text_size=30, title_pos='center', subtitle=sub_title, subtitle_text_size=25)
    bar.add('', name_list, num_list, title_pos='center', xaxis_interval=0, xaxis_rotate=27, xaxis_label_textsize=20,
            yaxis_label_textsize=20, yaxis_name_pos='end', yaxis_pos="%50")
    # bar.show_config()
    grid = Grid(width=1300, height=800)
    grid.add(bar, grid_top="13%", grid_bottom="23%", grid_left="15%", grid_right="15%")
    output_file = './chart/%s.html' % name
    grid.render(output_file)


def word_cloud(name, name_list, num_list, word_size_range):
    w_cloud = WordCloud(width=1400, height=900)
    w_cloud.add("", name_list, num_list, word_size_range=word_size_range, shape='pentagon')
    out_file_name = './chart/' + name + '.html'
    w_cloud.render(out_file_name)


def get_tag(text, counter):
    text = re.sub(r"<span.*><span>", "", text)
    tag_list = jieba.analyse.extract_tags(text)
    for tag in tag_list:
        counter[tag] += 1


def main():
    sex_dic = {1: '男性', 2: '女性', 0: '未知'}

    # log in
    itchat.auto_login(hotReload=True)
    friends = itchat.get_friends()
    download_images(friends)
    save_data(friends)
    if os.access('./json_data/friends.json', os.R_OK):
        with codecs.open('./json_data/friends.json', encoding='utf-8') as f:
            friends = json.load(f)

        # 待统计参数
        sex_counter = Counter()  # 性别
        nickname_list = []  # 昵称
        province_counter = Counter()  # 省份
        sign_counter = Counter()  # 签名

        for friend in friends:
            sex_counter[sex_dic[friend['Sex']]] += 1  # 统计性别
            nickname_list.append(friend['NickName'])  # 统计昵称
            get_tag(friend['Signature'], sign_counter)  # 提取签名关键词
            if friend['Province'] != '':
                province_counter[friend['Province']] += 1  # 统计省份

        # 性别饼图
        print(sex_counter)
        name_list, num_list = dict2list(sex_counter)
        get_pie('性别统计', name_list, num_list)

        # 省份饼图
        print(province_counter)
        name_list = []
        num_list = []
        prov_list = province_counter.most_common(6)
        for prov in prov_list:
            name_list.append(prov[0])
            num_list.append(prov[1])
        get_bar('省份统计', name_list, num_list)

        # 昵称云图
        num_list = [5 for i in range(1, len(nickname_list) + 1)]
        word_cloud('微信好友昵称', nickname_list, num_list, [18, 18])

        # 签名关键字云图
        name_list = []
        num_list = []
        tag_list = sign_counter.most_common(200)
        for tag in tag_list:
            name_list.append(tag[0])
            num_list.append(tag[1])
        word_cloud('微信好友签名关键词', name_list, num_list, [20, 100])

    itchat.logout()


if __name__ == '__main__':
    main()
