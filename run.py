import argparse  # argparseモジュールをインポート
from dotenv import load_dotenv
import os
from image_scraper import create_sub_dir, get_image_urls, save_images
from remove_bg import remove_background_from_images  # remove_bg.pyから関数をインポート

# .envファイルから環境変数を読み込む
load_dotenv()

def main(search_word):
    """
    メインの処理を行います。
    """
    api_key = os.getenv("API_KEY")
    cx = os.getenv("CX")
    save_dir = "./dlfiles"
    img_urls = get_image_urls(search_word, api_key, cx)
    save_sub_dir = create_sub_dir(save_dir)
    save_images(img_urls, save_sub_dir)

    # 背景を削除する
    remove_background_from_images(save_sub_dir, f"{save_sub_dir}_no_bg")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Googleから画像を検索し、ダウンロードした画像をリサイズします。')
    parser.add_argument('--query', type=str, required=True, help='Googleで画像を検索するためのキーワード')
    args = parser.parse_args()

    main(args.query)