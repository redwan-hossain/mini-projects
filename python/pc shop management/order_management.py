from abc import ABC, abstractmethod
from enum import Enum


class Products(Enum):
    KEYBOARD = 20
    MOUSE = 6
    MONITOR = 100
    SSD = 17


class Order:
    def __init__(self):
        self.ordered = []
        self.checkout_price: int = 0

    def take_order(self) -> list:
        while True:
            choice: int = int(input("enter desired product id: "))
            match choice:
                case 0:
                    break
                case 1:
                    self.ordered.append(Products.KEYBOARD.value)
                case 2:
                    self.ordered.append(Products.MOUSE.value)
                case 3:
                    self.ordered.append(Products.MONITOR.value)
                case 4:
                    self.ordered.append(Products.SSD.value)
        return self.ordered

    def cart(self) -> int:
        print("PC MART")
        print("Product List")
        for i, product in enumerate(Products):
            print(f"{i + 1}:", product.name.capitalize())
        print("0: Exit")
        self.take_order()
        return self.checkout(self.ordered)

    def checkout(self, products_in_cart: list) -> int:
        for price in products_in_cart:
            self.checkout_price += price
        return self.checkout_price


class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount):
        pass


class DebitCard(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code

    def pay(self, amount):
        print(f"Verifying security code: {self.security_code}")
        return f"Thanks, you have paid {amount}$"


class Paypal(PaymentProcessor):
    def __init__(self, email):
        self.email = email

    def pay(self, amount):
        print(f"Verifying security code: {self.email}")
        return f"Thanks, you have paid {amount}$"


demo = Order()
result = demo.cart()
customer_01 = DebitCard(1515)
print(customer_01.pay(result))
