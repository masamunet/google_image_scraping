import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

from image_resizer import resize_image

def get_image_urls(search_term, api_key, cx, num_results=100):
    """
    Google Custom Search JSON APIを使用して画像のURLを取得します。

    Args:
        search_term (str): 検索語句。
        api_key (str): APIキー。
        cx (str): 検索エンジンID。
        num_results (int): 取得する検索結果の数。

    Returns:
        list: 画像のURLのリスト。
    """
    url = "https://www.googleapis.com/customsearch/v1"
    img_urls = []
    for start in range(1, num_results, 10):  # 10件ずつ結果を取得
        params = {
            "q": search_term,
            "key": api_key,
            "cx": cx,
            "searchType": "image",
            "start": start,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        search_results = response.json()
        img_urls += [item["link"] for item in search_results["items"]]
    return img_urls

def download_image(url, file_path):
    """
    指定したURLから画像をダウンロードし、指定したパスに保存します。

    Args:
        url (str): ダウンロードする画像のURL。
        file_path (str): 画像を保存するパス。
    """
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(r.content)

def create_sub_dir(save_dir):
    """
    指定したディレクトリにサブディレクトリを作成します。

    Args:
        save_dir (str): サブディレクトリを作成するディレクトリのパス。

    Returns:
        str: 作成したサブディレクトリのパス。
    """
    now = datetime.now()
    sub_dir = now.strftime("%Y-%m-%d_%H_%M_%S")  # 秒も含めるようにフォーマットを変更
    save_sub_dir = os.path.join(save_dir, sub_dir)
    os.makedirs(save_sub_dir, exist_ok=True)
    return save_sub_dir

def save_images(img_urls, save_sub_dir):
    """
    指定したURLの画像をダウンロードし、指定したディレクトリに保存します。

    Args:
        img_urls (list): ダウンロードする画像のURLのリスト。
        save_sub_dir (str): 画像を保存するディレクトリのパス。
    """
    for index, url in enumerate(img_urls):
        file_name = "{}.jpg".format(index)
        image_path = os.path.join(save_sub_dir, file_name)
        download_image(url=url, file_path=image_path)
        resize_image(image_path)
