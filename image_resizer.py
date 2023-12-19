from PIL import Image
import PIL

def resize_image(image_path, min_size=512):
    """
    画像の短辺が指定したサイズ以上になるように、アスペクト比を保持したまま画像を拡大します。

    Args:
        image_path (str): 画像ファイルのパス。
        min_size (int): 画像の短辺の最小サイズ（ピクセル）。

    Returns:
        None
    """
    try:
        img = Image.open(image_path)
    except Exception as e:
        # 画像をオープンできなかった場合は処理を飛ばす
        print(f"画像を開くことができませんでした: {e}")
        return
    width, height = img.size
    if min(width, height) < min_size:
        ratio = max(min_size / width, min_size / height)
        new_size = (int(width * ratio), int(height * ratio))
        img = img.resize(new_size, PIL.Image.LANCZOS)
        try:
            img.save(image_path)
        except:
            return