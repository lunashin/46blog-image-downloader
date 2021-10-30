#!/usr/bin/python3

import os
import sys
import pprint
import time
import datetime
import urllib.error
import urllib.request

import requests
from bs4 import BeautifulSoup

from urllib.parse import urlparse



# check argument
# args = sys.argv
# if (len(args) != 3):
#     print("櫻坂ブログから画像を取得します。")
#     print("*.py [各メンバーのブログ一覧ページの URL] [save dir]")
#     print("")
#     print("ex) *.py https://sakurazaka46.com/s/s46/diary/blog/list?ima=2722&ct=11 ./sugai")
#     sys.exit(1)


# URL
# load_url = "https://sakurazaka46.com/s/s46/diary/blog/list?ima=2722&ct=11"
# download_dest = args[2]
# base_url = urlparse(load_url).scheme + "://" + urlparse(load_url).netloc

# after filr
after_file = "./after"

# log
logfile="./sakura-img-dl.log"

# base dir
base_dir = "./img/"


#------------------------------------------
# functions
#------------------------------------------

# ファイルダウンロード
def download_file(url, dst_path):
    log("download img: " + url)
    print("download img: " + url)
    try:
        with urllib.request.urlopen(url) as web_file:
            data = web_file.read()
            with open(dst_path, mode='wb') as local_file:
                local_file.write(data)
    except urllib.error.URLError as e:
        print(e)


# ファイルダウンロード(出力先ディレクトリを指定)
def download_file_to_dir(url, dst_dir, prefix):
    download_file(url, os.path.join(dst_dir, prefix + "-" + os.path.basename(url)))


# ダウンロード済みリストへ追記
def add_after(url):
    log("Add after: " + url)
    with open(after_file, mode='a') as f:
        f.write("\n")
        f.write(url)

# ダウンロード済みリストにURLが存在するか確認
def is_after(url):
    if url == None:
        return False
    log("Check: " + str(url))
    with open(after_file) as f:
        for i, line in enumerate(f):
            if url in line:
                return True
    return False


# ログ出力
def log(log_str):
    with open(logfile, mode='a') as f:
        f.write("\n")
        dt_now = datetime.datetime.now()
        f.write(dt_now.strftime('%Y-%m-%d %H:%M:%S'))
        f.write(" ")
        f.write(log_str)


# メンバーのブログ一覧から各ブログへアクセスして画像ダウンロード
def download_sakura_img(target_url, dest_dir):
    log("try: " + target_url)
    # 保存先ディレクトリ作成
    os.makedirs(dest_dir, exist_ok=True)

    base_url = urlparse(target_url).scheme + "://" + urlparse(target_url).netloc

    # サイト取得
    log("get list: " + target_url)
    html = requests.get(target_url)
    soup = BeautifulSoup(html.content, "html.parser")

    #blog_listm = soup.find(class_="member-blog-listm")
    blog_listm = soup.find(class_="com-blog-part")

    # 各ブログのリンク取得
    for element in blog_listm.find_all("a"):
        blog_url = base_url + element.get("href")
        print("Blog URL: " + blog_url) 

        # すでに取得済みページか確認
        # if is_after(blog_url) == True:
        #     log("Already processed: " + blog_url)
        #     continue

        # URLのページIDをファイルのprefixにする
        prefix = os.path.basename(urlparse(blog_url).path)

        # ブログページから画像ダウンロード
        log("get blog: " + blog_url)
        html2 = requests.get(blog_url)
        soup2 = BeautifulSoup(html2.content, "html.parser")
        blog_article = soup2.find(class_="box-article")
        for elem_img in blog_article.find_all("img"):
            img_url = elem_img.get("src")
            if img_url == None:
                print("img url is None") 
                continue
            print("img url: " + img_url) 
            if is_after(img_url) == True:
                log("Skip (Already get): " + img_url)
                print("Skip (Already get): " + img_url)
                continue
            download_file_to_dir(base_url + img_url, dest_dir, prefix)
            # 処理済みURL追記
            add_after(img_url)



#------------------------------------------
# main
#------------------------------------------

# 1期生
download_sakura_img("https://sakurazaka46.com/s/s46/diary/blog/list?ima=5731&ct=07", base_dir + "1-kobayashi")
download_sakura_img("https://sakurazaka46.com/s/s46/diary/blog/list?ima=0743&ct=03", base_dir + "1-uemura")
download_sakura_img("https://sakurazaka46.com/s/s46/diary/blog/list?ima=1859&ct=11", base_dir + "1-sugai")
download_sakura_img("https://sakurazaka46.com/s/s46/diary/blog/list?ima=1539&ct=08", base_dir + "1-saito")
download_sakura_img("https://sakurazaka46.com/s/s46/diary/blog/list?ima=2241&ct=06", base_dir + "1-koike")
download_sakura_img("https://sakurazaka46.com/s/s46/diary/blog/list?ima=0719&ct=21", base_dir + "1-risa")
download_sakura_img("https://sakurazaka46.com/s/s46/diary/blog/list?ima=3113&ct=20", base_dir + "1-rika")
download_sakura_img("https://sakurazaka46.com/s/s46/diary/blog/list?ima=3113&ct=04", base_dir + "1-ozeki")
download_sakura_img("https://sakurazaka46.com/s/s46/diary/blog/list?ima=5440&ct=18", base_dir + "1-moriya")

# 2期生
download_sakura_img("https://sakurazaka46.com/s/s46/diary/blog/list?ima=3702&ct=54", base_dir + "2-ozono")
download_sakura_img("https://sakurazaka46.com/s/s46/diary/blog/list?ima=2852&ct=45", base_dir + "2-takemoto")
download_sakura_img("https://sakurazaka46.com/s/s46/diary/blog/list?ima=1453&ct=47", base_dir + "2-karin")
download_sakura_img("https://sakurazaka46.com/s/s46/diary/blog/list?ima=2806&ct=56", base_dir + "2-kosaka")
download_sakura_img("https://sakurazaka46.com/s/s46/diary/blog/list?ima=1859&ct=43", base_dir + "2-inoue")
download_sakura_img("https://sakurazaka46.com/s/s46/diary/blog/list?ima=2125&ct=50", base_dir + "2-morita")
download_sakura_img("https://sakurazaka46.com/s/s46/diary/blog/list?ima=1355&ct=55", base_dir + "2-oonuma")
download_sakura_img("https://sakurazaka46.com/s/s46/diary/blog/list?ima=1006&ct=44", base_dir + "2-seki")
download_sakura_img("https://sakurazaka46.com/s/s46/diary/blog/list?ima=1102&ct=48", base_dir + "2-matsuda")
download_sakura_img("https://sakurazaka46.com/s/s46/diary/blog/list?ima=5731&ct=51", base_dir + "2-ten")
download_sakura_img("https://sakurazaka46.com/s/s46/diary/blog/list?ima=0342&ct=46", base_dir + "2-tamura")
download_sakura_img("https://sakurazaka46.com/s/s46/diary/blog/list?ima=5400&ct=57", base_dir + "2-kira")
