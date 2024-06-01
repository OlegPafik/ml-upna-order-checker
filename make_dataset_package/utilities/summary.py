def marking_plates(orders):
    marking_plates = [order.marking_plate for order in orders]
    print(marking_plates)

def backups(orders):
    backups = [order.backup for order in orders]
    print(backups)

def product_types(orders):
    products = [order.product_type for order in orders]
    print(products)

def count_sensors(orders):
    products = [order.product_type for order in orders]
    sensors = [product for product in products if 'sensor' in product]
    print(len(sensors))

def count_devices(orders):
    products = [order.product_type for order in orders]
    devices = [product for product in products if 'device' in product]
    print(len(devices))