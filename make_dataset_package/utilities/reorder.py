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


def for_device_sensor_orientation_OK(input_path, output_path):
    __create_device_sensor_folders_if_necessary(output_path)
    for subset in ['train', 'test']:
        images_filenames = __get_images_filenames(f'{input_path}/{subset}/OK')
        regex_device = re.compile(r".*\_device.jpg", re.IGNORECASE)
        regex_sensor = re.compile(r".*\_sensor.jpg", re.IGNORECASE)
        for image_filename in images_filenames:
            image = Image.open(f'{input_path}/{subset}/OK/{image_filename}')
            if regex_device.match(image_filename):
                image.save(f'{output_path}/{subset}/device/{image_filename}')
            elif regex_sensor.match(image_filename):
                image.save(f'{output_path}/{subset}/sensor/{image_filename}')


def copy_paste_images(input_path, output_path):
    images_filenames = __get_images_filenames(input_path)
    __copy_paste(images_filenames, input_path, output_path)

def create_orientation_train_test_folders_if_necessary(path):
    paths = [path,
             path + '/train/OK',
             path + '/train/NOK',
             path + '/test/OK',
             path + '/test/NOK']
    
    for desired_path in paths:
        if not os.path.exists(desired_path):
            os.makedirs(desired_path)
            print(f"Folder {desired_path} created.")

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