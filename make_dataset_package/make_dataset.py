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

def device_sensor_orientation_OK():
    input_path = 'datasets/orientation'
    output_path = 'datasets/device_sensor_orientation_OK'
    reorder.for_device_sensor_orientation_OK(input_path, output_path)

def just_rotate():
    path = 'datasets/orientation/train/NOK'
    rotate.just_rotate(path)
    path = 'datasets/orientation/test/NOK'
    rotate.just_rotate(path)

def create_rotated():
    input_path = 'datasets/orientation/train/OK'
    output_path = 'datasets/orientation/train/NOK'
    rotate.create_rotated(input_path, output_path)
    input_path = 'datasets/orientation/test/OK'
    output_path = 'datasets/orientation/test/NOK'
    rotate.create_rotated(input_path, output_path)

def copy_all_marking_plates_in_orientation_NOK():
    reorder.create_orientation_train_test_folders_if_necessary('datasets/orientation')
    for subset in ['train', 'test']:
        input_paths = [f'datasets/device_sensor/{subset}/device',
                       f'datasets/device_sensor/{subset}/sensor']
        output_path = f'datasets/orientation/{subset}/NOK'
        for input_path in input_paths:
            reorder.copy_paste_images(input_path, output_path)

def print_count():
    print('Devices count:')
    summary.count_devices(orders)
    print('Sensors count:')
    summary.count_sensors(orders)
