from .factories import order_factory
from .utilities import summary
from .utilities import reorder
from .utilities import rotate

orders_folders_path = 'PR-Orden de fabricacion'
orders = order_factory.create_orders(orders_folders_path)

def device_sensor():
    output_path = 'datasets/device_sensor'
    reorder.for_device_sensor(orders, orders_folders_path, output_path)

def backups():
    output_path = 'datasets/backups'
    reorder.for_backups(orders, orders_folders_path, output_path)

def just_rotate():
    path = 'datasets/orientation/NOK'
    rotate.just_rotate(path)

def create_rotated():
    input_path = 'datasets/orientation/OK'
    output_path = 'datasets/orientation/NOK'
    rotate.create_rotated(input_path, output_path)

def copy_all_marking_plates_in_orientation_NOK():
    input_paths = ['datasets/device_sensor/train/device',
                   'datasets/device_sensor/train/sensor',
                   'datasets/device_sensor/test/device',
                   'datasets/device_sensor/test/sensor']
    output_path = 'datasets/orientation/NOK'
    for input_path in input_paths:
        reorder.copy_all_marking_plates_in_orientation_NOK(input_path, output_path)

def print_count():
    print('Devices count:')
    summary.count_devices(orders)
    print('Sensors count:')
    summary.count_sensors(orders)
