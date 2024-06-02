import os
import random
import re
import shutil
from PIL import Image

def for_device_sensor(orders, orders_folders_path, output_path):
    __create_device_sensor_folders_if_necessary(output_path)
    orders_train, orders_test = __split_train_test(orders, ratio_train = 0.8)

    for order in orders_train:
        try:
            source_file = orders_folders_path + '/' + order.folder + '/' + order.marking_plate
            end_file = output_path + '/train/' + order.product_type + '/' + order.marking_plate
            __save_resized(source_file, end_file)
        except Exception as e:
            print(f"Error copy/pasting images: {e}")
    
    for order in orders_test:
        try:
            source_file = orders_folders_path + '/' + order.folder + '/' + order.marking_plate
            end_file = output_path + '/test/' + order.product_type + '/' + order.marking_plate
            __save_resized(source_file, end_file)
        except Exception as e:
            print(f"Error copy/pasting images: {e}")


def for_backups(orders, orders_folders_path, output_path):
    __create_backup_folders_if_necessary(output_path)

    for order in orders:
        try:
            source_file = orders_folders_path + '/' + order.folder + '/' + order.backup
            end_file = output_path + '/' + order.product_type + '/' + order.backup
            shutil.copy(source_file, end_file)
        except Exception as e:
            print(f"Error copy/pasting images: {e}")

def copy_paste_images(input_path, output_path):
    images_filenames = __get_images_filenames(input_path)
    __copy_paste(images_filenames, input_path, output_path)

def split_train_test_orientation(path):
    for category in ['OK', 'NOK']:
        images_filenames = __get_images_filenames(path + '/' + category)
        images_filenames_train, images_filenames_test = __split_train_test(images_filenames, ratio_train = 0.8)
        __create_orientation_train_test_folders_if_necessary(path, category)
        __copy_paste(images_filenames_train, path + '/' + category, path + '/train/' + category)
        __copy_paste(images_filenames_test, path + '/' + category, path + '/test/' + category)

def __split_train_test(samples, ratio_train, shuffle = True):
    if shuffle == True:
        random.shuffle(samples)
    split_index = round(len(samples) * ratio_train)
    samples_train = samples[:split_index]
    samples_test = samples[split_index:]
    return samples_train, samples_test

def __create_device_sensor_folders_if_necessary(path):
    paths = [path,
             path + '/train/device',
             path + '/train/sensor',
             path + '/test/device',
             path + '/test/sensor']
    
    for desired_path in paths:
        if not os.path.exists(desired_path):
            os.makedirs(desired_path)
            print(f"Folder {desired_path} created.")


def __create_backup_folders_if_necessary(path):
    paths = [path,
             path + '/device',
             path + '/sensor']
    
    for desired_path in paths:
        if not os.path.exists(desired_path):
            os.makedirs(desired_path)
            print(f"Folder {desired_path} created.")

def __create_orientation_train_test_folders_if_necessary(path, category):
    paths = [path,
             path + '/train/' + category,
             path + '/test/' + category]
    
    for desired_path in paths:
        if not os.path.exists(desired_path):
            os.makedirs(desired_path)
            print(f"Folder {desired_path} created.")

def __save_resized(source_file, end_file):
    resize_factor = 0.25

    with Image.open(source_file) as img:
        new_size = (int (img.size[0]*resize_factor), int (img.size[1]*resize_factor))
        resized_img = img.resize(new_size, Image.LANCZOS)
        resized_img.save(end_file)

def __get_images_filenames(input_path):
    images_filenames = []
    regex = re.compile(r".*\.jpg", re.IGNORECASE)
    with os.scandir(input_path) as files:
            for file in files:
                if regex.match(file.name):
                    images_filenames.append(file.name)
    return images_filenames

def __copy_paste(image_filenames, input_path, output_path):
    for image_filename in image_filenames:
        image = Image.open(input_path + '/' + image_filename)
        if 'train/device' in input_path or 'test/device' in input_path:
            image.save(output_path + '/' + image_filename.replace('.', '_device.'))
        elif 'train/sensor' in input_path or 'test/sensor' in input_path:
            image.save(output_path + '/' + image_filename.replace('.', '_sensor.'))
        else:
            image.save(output_path + '/' + image_filename)