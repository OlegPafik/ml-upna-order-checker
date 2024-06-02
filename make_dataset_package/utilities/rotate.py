import os
import re
from PIL import Image

def create_rotated(input_path, output_path):
    images_filenames = __get_images_filenames(input_path)
    __create_output_folder_if_necessary(output_path)
    __save_rotated(images_filenames, input_path, output_path)
    
def __get_images_filenames(input_path):
    images_filenames = []
    regex = re.compile(r".*\.jpg", re.IGNORECASE)
    with os.scandir(input_path) as files:
            for file in files:
                if regex.match(file.name):
                    images_filenames.append(file.name)
    return images_filenames

def __create_output_folder_if_necessary(output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Folder {output_path} created.")

def __save_rotated(image_filenames, input_path, output_path):
    for image_filename in image_filenames:
        image = Image.open(input_path + '/' + image_filename)
        for degrees in [90, 180, 270]:
            rotated_image = image.rotate(degrees, expand=True)
            rotated_image.save(output_path + '/' + image_filename.replace('.', '_' + str(degrees) + 'deg.'))







