from .factories import order_factory
from .utilities import summary
from .utilities import reorder

orders_folders_path = 'PR-Orden de fabricacion'
orders = order_factory.create_orders(orders_folders_path)

def device_sensor():
    output_path = 'datasets/device_sensor'
    reorder.for_device_sensor(orders, orders_folders_path, output_path)

def backups():
    output_path = 'datasets/backups'
    reorder.for_backups(orders, orders_folders_path, output_path)

def print_count():
    print('Devices count:')
    summary.count_devices(orders)
    print('Sensors count:')
    summary.count_sensors(orders)