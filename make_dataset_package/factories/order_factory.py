import os
import re
from ..models.order import Order

__all__ = ['create_orders']

def create_orders(orders_folders_path):

    valid_orders_folders = __get_valid_orders_folders(orders_folders_path)

    orders = []
    for order_folder in valid_orders_folders:
        marking_plate = __get_marking_plate(orders_folders_path, order_folder)
        backup = __get_backup(orders_folders_path, order_folder)
        product_type = __get_product_type(backup)

        if (backup is not None and
            marking_plate is not None and 
            product_type is not None):

            order = Order(order_folder, backup, marking_plate, product_type)
            orders.append(order)

    return orders


def __get_valid_orders_folders(orders_folders_path):

    regex = re.compile(r"^PR-F12-\d{5}_\d{4}$")

    valid_orders = []

    with os.scandir(orders_folders_path) as orders_folders:
        for order_folder in orders_folders:
            if regex.match(order_folder.name):
                valid_orders.append(order_folder.name)
    
    return valid_orders


def __get_marking_plate(orders_folders_path, order_folder):

    order_folder_path = orders_folders_path + '/' + order_folder
    regex = re.compile(r"^Marking_plate_\d{4}.(png|jpg)$")
    
    with os.scandir(order_folder_path) as files:
        for file in files:
            if regex.match(file.name):
                return file.name
        return None
    

def __get_backup(orders_folders_path, order_folder):

    order_folder_path = orders_folders_path + '/' + order_folder
    regex = re.compile(r"^backup_\d{9}_\d{4}_\d{8}T\d{6}.json$")
    
    with os.scandir(order_folder_path) as files:
        for file in files:
            if regex.match(file.name):
                return file.name
        return None


def __get_product_type(backup):
    if backup is None: return None

    regex_device = re.compile(r"^backup_890110\d{3}_\d{4}_\d{8}T\d{6}.json$")
    regex_sensor = re.compile(r"^backup_891010\d{3}_\d{4}_\d{8}T\d{6}.json$")
    
    if regex_device.match(backup):
        return 'device'
    if regex_sensor.match(backup):
        return 'sensor'
    return None