class Order:
    folder = None
    backup = None
    marking_plate = None
    product_type = None

    def __init__(self, folder, backup, marking_plate, product_type):
        self.folder = folder
        self.backup = backup
        self.marking_plate = marking_plate
        self.product_type = product_type