from models.product import Product

class OrderItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
        self.price = product.price * quantity
    def __repr__(self):
        return f"OrderItem(product={self.product.name}, quantity={self.quantity}, price={self.price})"
    def update_quantity(self, new_quantity):
        self.quantity = new_quantity
        self.price = self.product.price * new_quantity
    def get_total_price(self):
        return self.price
    def to_dict(self):
        return {
            'product_id': self.product.id,
            'quantity': self.quantity,
            'price': self.price
        }
    def from_dict(cls, data):
        product = Product.get_by_id(data['product_id'])
        return cls(product, data['quantity'])
    @classmethod
    def get_by_id(cls, order_item_id):
        for item in cls.order_items:
            if item.id == order_item_id:
                return item
        return None
    @classmethod
    def get_all(cls):
        return cls.order_items
    order_items = [] 
    