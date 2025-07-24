from models.product import Product
import json
class Manager:
    def __init__(self):
        self.order_items = []
        self.order_items = []

    def add_order_item(self, order_item):
        self.order_items.append(order_item)

    def get_order_items(self):
        return self.order_items

    def remove_order_item(self, order_item_id):
        for item in self.order_items:
            if item.id == order_item_id:
                self.order_items.remove(item)
                return True
        return False

    def get_order_item_by_id(self, order_item_id):
        for item in self.order_items:
            if item.id == order_item_id:
                return item
        return None

    def get_order_items_as_products(self):
        products = []
        for item in self.order_items:
            product = Product.from_dict(item.product.to_dict())
            products.append(product)
        return products
    @classmethod
    def load_order_items_from_file(cls):
        try:
            with open('database/order_items.json', encoding="utf-8") as jsonfile:
                data = json.load(jsonfile)
        except FileNotFoundError:
            return []
        return [OrderItem.from_dict(item) for item in data]
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
    @classmethod
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

    @classmethod
    def get_products_from_order_items(cls):
        products = []
        for item in cls.order_items:
            product = Product.from_dict(item)
            products.append(product)
        return products
from datetime import datetime
from uuid import uuid4
from utils import (
    make_password, is_valid_username, print_status,
    is_valid_password,
)


class User:
    
    def __init__(self, id, username, password, phone, first_name, last_name, age, gender):
        self.id = id
        self.username = username
        self.password = password
        self.phone = phone
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.joined_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'phone': self.phone,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'gender': self.gender,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['id'],
            data['username'],
            data['password'],
            data['phone'],
            data['first_name'],
            data['last_name'],
            data['age'],
            data['gender'],
        )
    
    @classmethod
    def load_users(cls):
        try:
            with open('database/users.json', encoding="utf-8") as jsonfile:
                data = json.load(jsonfile)
        except :
            data = []
        users = [User.from_dict(item) for item in data]
        return users

    @classmethod
    def save_users(cls, users):
        with open('database/users.json', 'w', encoding="utf-8") as jsonfile:
            data = [user.to_dict() for user in users]
            json.dump(data, jsonfile, indent=2)

    @classmethod
    def create_user(cls):
        username = input("Username: ")
        password = input("Password: ")
        confirm_password = input("Confirm Password: ")
        phone = input("Phone: ")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        age = input("Age: ")
        gender = input("Gender: ")

        if not is_valid_username(username):
            print_status("username xato kiritildi.", "error")
        elif User.check_username(username):
            print_status("username tanlangean.", 'error')
        elif not is_valid_password(password):
            print_status("password xato kiritildi.", "error")
        elif password != confirm_password:
            print_status("password va confirm password mos emas.", "error")
        else:
            user = cls(str(uuid4()), username, make_password(password), phone, first_name, last_name, age, gender)
            users = cls.load_users()
            users.append(user)
            cls.save_users(users)

    @classmethod
    def check_username(cls, username: str):
        for user in User.load_users():
            if user.username == username:
                return True
            
        return False
