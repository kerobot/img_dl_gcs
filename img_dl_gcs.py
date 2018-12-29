import os
import sys
import json
import settings
import requests
from urllib.parse import quote

# https://qiita.com/too-ai/items/4fad0239b8b3c465fe6d
# https://blog.aidemy.net/entry/2017/12/17/214715

# 画像
# https://qiita.com/onlyzs/items/c56fb76ce43e45c12339
# https://github.com/onlyzs89/study/blob/master/collectImagenet.py

# ノウハウ
# https://note.nkmk.me/python-split-strip-list-join/
# https://note.nkmk.me/python-f-strings/

# git clone <<URL>>

# git status
# git add -A
# git status
# git commit -m "xxxxx"
# git remote add origin <<URL>>
# git push origin master

# git fetch
# git merge --allow-unrelated-histories origin/master

# git pull origin master

# 指定したキーワードで検索した画像のURLを取得
def get_image_urls(keyword, total_num):
    image_urls = []
    i = 0
    while i < total_num:
        # クエリの組み立て
        query = CUSTOM_SEARCH_URL + "?key=" + settings.API_KEY + \
                "&cx=" + settings.CUSTOM_SEARCH_ENGINE + "&num=" + \
                str(10 if(total_num-i)>10 else (total_num-i)) + "&start=" + \
                str(i+1) + "&q=" + quote(keyword) + "&searchType=image"
        print (query)
        # GETリクエスト
        response = requests.get(query)
        # JSONデータ取得
        json = response.json()
        # 10件ずつのURLを格納
        for j in range(len(json["items"])):
            image_urls.append(json["items"][j]["link"])
        i=i+10
    return image_urls

# 画像のURLをもとに画像をダウンロードして保存
def get_image_files(dir_path, keyword, image_urls):
    # 画像urlループ
    for i in range(len(image_urls)):
        try:
            # 画像をダウンロード
            print(image_urls[i])
            image = download_image(image_urls[i])
            # ファイル名を作成
            filename_extension_pair = os.path.splitext(image_urls[i])
            extension = filename_extension_pair[1]
            extension = extension if len(extension) <= 4 else extension[0:4]
            filename = os.path.join(dir_path, keyword+"_"+f"{i+1:03}"+extension)
            print(filename)
            # 画像をファイルとして保存
            save_image(filename, image)
        except RuntimeError as e:
            print(f"type:{type(e)}")
            print(f"args:{e.args}")
            print(f"{e}")
            continue
        except BaseException as e:
            print(f"type:{type(e)}")
            print(f"args:{e.args}")
            print(f"{e}")
            continue

# 画像をダウンロード
def download_image(url):
    response = requests.get(url, timeout=100)
    if response.status_code != 200:
        raise RuntimeError("画像が取得できません")
    content_type = response.headers["content-type"]
    if 'image' not in content_type:
        raise RuntimeError("画像ではありません")
    return response.content

# 画像をファイルとして保存
def save_image(filename, image):
    with open(filename, "wb") as file:
        file.write(image)

RETURN_SUCCESS = 0
RETURN_FAILURE = -1

# Custom Search Url
CUSTOM_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

# Download Directory Path
ORIGIN_IMAGE_DIR = "./origin_image"

def main():
    print("===================================================================")
    print("イメージダウンローダー Google Customr Search API 版")
    print("指定したキーワードに一致する画像ファイルをダウンロードします。")
    print("===================================================================")

    # 引数のチェック
    argvs = sys.argv
    if len(argvs) != 2 or len(argvs[1]) == 0:
        print("キーワードを指定してください。")
        return RETURN_FAILURE

    # キーワードの取得
    keywords = [x.strip() for x in argvs[1].split(',')]

    # ディレクトリの作成
    if os.path.isdir(ORIGIN_IMAGE_DIR) == False:
        os.mkdir(ORIGIN_IMAGE_DIR)

    # キーワードごとに画像ファイル取得
    for keyword in keywords:
        # キーワード表示
        print(keyword)
        # 画像URL取得
        image_urls = get_image_urls(keyword, 100)
        # 画像ファイルダウンロード
        get_image_files(ORIGIN_IMAGE_DIR, keyword, image_urls)

    return RETURN_SUCCESS

if __name__ == "__main__":
    sys.exit(main())
