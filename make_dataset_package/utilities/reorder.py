import os
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


def __split_train_test(orders, ratio_train):
    split_index = round(len(orders) * ratio_train)
    orders_train = orders[:split_index]
    orders_test = orders[split_index:]
    return orders_train, orders_test


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