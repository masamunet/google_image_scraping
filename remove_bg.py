import rembg
import os
from PIL import Image
import PIL  # PILモジュールを追加
import numpy as np  # numpyモジュールを追加

def remove_background_from_images(input_directory, output_directory):
    """
    指定されたディレクトリ内のすべての画像ファイルから背景を削除します。

    Args:
        input_directory (str): 画像ファイルが含まれるディレクトリのパス。
        output_directory (str): 背景が削除された画像を保存するディレクトリのパス。
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, filename)
            output_path = output_path.rsplit('.', 1)[0] + '.jpg'  # Change the output format to JPEG
            try:
                with open(input_path, "rb") as input_file:
                    image = Image.open(input_file)
                    output = rembg.remove(image)
                    # Convert the image to RGBA if it's not already
                    if output.mode != 'RGBA':
                        output = output.convert('RGBA')
                    # Create a white image of the same size
                    white_bg = Image.new('RGBA', output.size, 'WHITE')
                    # Paste the output image on top of the white background
                    final_output = Image.alpha_composite(white_bg, output)
                    # Convert the image to RGB
                    final_output = final_output.convert('RGB')

                    # Convert the image to a numpy array
                    np_image = np.array(final_output)

                    # Find the non-white pixels
                    non_white_pixels = np.where((np_image != [255, 255, 255]).all(axis=2))

                    # Get the coordinates of the non-white pixels
                    y_min, y_max = np.min(non_white_pixels[0]), np.max(non_white_pixels[0])
                    x_min, x_max = np.min(non_white_pixels[1]), np.max(non_white_pixels[1])

                    # Calculate the center of the non-white pixels
                    center_y, center_x = (y_min + y_max) // 2, (x_min + x_max) // 2

                    # Calculate the length of the maximum dimension
                    max_dim = max(y_max - y_min, x_max - x_min)

                    # Calculate the coordinates of the cropped image
                    y_min_crop = max(0, center_y - max_dim // 2)
                    y_max_crop = min(np_image.shape[0], center_y + max_dim // 2)
                    x_min_crop = max(0, center_x - max_dim // 2)
                    x_max_crop = min(np_image.shape[1], center_x + max_dim // 2)

                    # Crop the image
                    cropped_image = final_output.crop((x_min_crop, y_min_crop, x_max_crop, y_max_crop))

                    # Save the cropped image
                    cropped_image.save(output_path)
            except PIL.UnidentifiedImageError:
                print(f"警告: {input_path} は画像ファイルではないためスキップされました。")

if __name__ == "__main__":
    sub_dir = os.getenv('SUB_DIR', 'test_sample_sub_dir')
    remove_background_from_images(f"./dlfiles/{sub_dir}", f"./dlfiles/no_bg_{sub_dir}")