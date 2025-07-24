from models.order_item import OrderItem

class Order:
    def __init__(self, customer):
        self.customer = customer
        self.items = []
    def add_item(self, product, quantity):
        item = OrderItem(product, quantity)
        self.items.append(item)
    def remove_item(self, item):
        self.items.remove(item)
    def get_total(self):
        return sum(item.get_total_price() for item in self.items)
    def to_dict(self):
        return {
            'customer': self.customer,
            'items': [item.to_dict() for item in self.items]
        }
    @classmethod
    def from_dict(cls, data):
        order = cls(data['customer'])
        for item_data in data['items']:
            item = OrderItem.from_dict(item_data)
            order.add_item(item.product, item.quantity)
        return order
    @classmethod
    def get_by_id(cls, order_id):
        for order in cls.orders:
            if order.id == order_id:
                return order
        return None 
    @classmethod
    def get_all(cls):
        return cls.orders
    orders = []  