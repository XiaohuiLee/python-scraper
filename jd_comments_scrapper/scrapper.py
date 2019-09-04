import os
import time
import json
import random

import jieba
import requests
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud

os.chdir('C:/Users/Aukuno/Desktop/Lab/jd_comments_scrapper')

# 词云形状图片
WC_MASK_IMG = 'dog.jpg'
# 评论数据保存文件
COMMENT_FILE_PATH = 'jd_comment.txt'
# 词云字体
WC_FONT_PATH = 'msyhl.ttc'
# 产品ID
PRODUCT_ID = '100001956891'

def spider_comment(page=0):
    """
    爬取京东指定页的评价数据
    :param page: 爬取第几，默认值为0
    """
    url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1441&productId=%s&score=0&sortType=5&page=%s&pageSize=10&isShadowSku=0&fold=1' % (PRODUCT_ID, page)
    kv = {'user-agent': 'Mozilla/5.0', 'Referer': 'https://item.jd.com/{}.html'.format(PRODUCT_ID)}

    try:
        r = requests.get(url, headers=kv)
        r.raise_for_status()
    except:
        print('爬取失败')
    # 截取json数据字符串
    r_json_str = r.text[26:-2]
    # 字符串转json对象
    r_json_obj = json.loads(r_json_str)
    # 获取评价列表数据
    r_json_comments = r_json_obj['comments']
    # 遍历评论对象列表
    print('正在爬取第{}页...'.format(str(page)))
    for r_json_comment in r_json_comments:
        # 以追加模式换行写入每条评价
        with open(COMMENT_FILE_PATH, 'a+') as file:
            file.write(r_json_comment['content'] + '\n')
        # 打印评论对象中的评论内容


def batch_spider_comment():
    """
    批量爬取某东评价
    """
    # 写入数据前先清空之前的数据
    if os.path.exists(COMMENT_FILE_PATH):
        os.remove(COMMENT_FILE_PATH)
    for i in range(50):
        spider_comment(i)
        # 模拟用户浏览，设置一个爬虫间隔，防止ip被封
        time.sleep(random.random() * 5)


def cut_word():
    """
    对数据分词
    :return: 分词后的数据
    """
    with open(COMMENT_FILE_PATH) as file:
        comment_txt = file.read()
        wordlist = jieba.cut(comment_txt, cut_all=True)
        wl = " ".join(wordlist)
        print(wl)
        return wl


def create_word_cloud():
    """
    生成词云
    :return:
    """
    # 设置词云形状图片
    wc_mask = np.array(Image.open(WC_MASK_IMG))
    # 设置词云的一些配置，如：字体，背景色，词云形状，大小
    wc = WordCloud(background_color="white", max_words=2000, mask=wc_mask, scale=4,
                   max_font_size=50, random_state=42, font_path=WC_FONT_PATH)
    # 生成词云
    wc.generate(cut_word())

    # 在只设置mask的情况下,你将会得到一个拥有图片形状的词云
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    # plt.figure()
    plt.show()


if __name__ == '__main__':
    # 爬取数据
    batch_spider_comment()

    # 生成词云
    create_word_cloud()