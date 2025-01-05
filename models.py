from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# Модель пользователя для работы с ролями (админ и пользователь)
class User(UserMixin, db.Model):
    __tablename__ = 'users'  # Название таблицы пользователей в БД
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(50))  # Роль ('admin' или 'user')

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role


# Модели для таблиц базы данных
class Supplier(db.Model):
    __tablename__ = 'suppliers'

    supplier_id = db.Column('supplier_id', db.BigInteger, primary_key=True)
    company_name = db.Column('company_name', db.String(100))
    contact_phone = db.Column('contact_phone', db.String(20))
    cooperation_date = db.Column('cooperation_date', db.Date)

    deliveries = relationship('Delivery', back_populates='supplier', lazy='dynamic')


class Employee(db.Model):
    __tablename__ = 'employees'

    employee_id = db.Column('employee_id', db.BigInteger, primary_key=True)
    employee_name = db.Column('employee_name', db.String(100))
    position = db.Column('position', db.String(50))
    salary = db.Column('salary', db.Numeric(10, 2))
    contract_date = db.Column('contract_date', db.Date)

    deliveries = relationship('Delivery', back_populates='employee', lazy='dynamic')
    orders = relationship('Order', back_populates='employee', lazy='dynamic')


class Delivery(db.Model):
    __tablename__ = 'deliveries'

    delivery_id = db.Column('delivery_id', db.BigInteger, primary_key=True)
    delivery_date = db.Column('delivery_date', db.Date)
    supplier_id = db.Column(db.BigInteger, ForeignKey('suppliers.supplier_id', ondelete='CASCADE'))
    employee_id = db.Column(db.BigInteger, ForeignKey('employees.employee_id', ondelete='CASCADE'))

    delivery_details = relationship('DeliveryDetail', back_populates='delivery', lazy='dynamic')
    supplier = relationship('Supplier', back_populates='deliveries')
    employee = relationship('Employee', back_populates='deliveries')


class Bouquet(db.Model):
    __tablename__ = 'bouquets'

    bouquet_id = db.Column('bouquet_id', db.BigInteger, primary_key=True)
    name = db.Column('name', db.String(100))
    price = db.Column('price', db.Numeric(10, 2))
    description = db.Column('description', db.Text)

    products = relationship('Product', back_populates='bouquet', lazy='dynamic')


class Flower(db.Model):
    __tablename__ = 'flowers'

    flower_id = db.Column('flower_id', db.BigInteger, primary_key=True)
    shelf_life = db.Column('shelf_life', db.Integer)
    description = db.Column('description', db.Text)
    price = db.Column('price', db.Numeric(10, 2))

    products = relationship('Product', back_populates='flower', lazy='dynamic')


class AdditionalMaterial(db.Model):
    __tablename__ = 'additional_materials'

    material_id = db.Column('material_id', db.BigInteger, primary_key=True)
    description = db.Column('description', db.Text)

    products = relationship('Product', back_populates='material', lazy='dynamic')


class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column('product_id', db.BigInteger, primary_key=True)
    product_name = db.Column('product_name', db.String(100))
    unit_price = db.Column('unit_price', db.Numeric(10, 2))
    bouquet_id = db.Column(db.BigInteger, ForeignKey('bouquets.bouquet_id', ondelete='SET NULL'), nullable=True)
    flower_id = db.Column(db.BigInteger, ForeignKey('flowers.flower_id', ondelete='SET NULL'), nullable=True)
    material_id = db.Column(db.BigInteger, ForeignKey('additional_materials.material_id', ondelete='SET NULL'), nullable=True)

    bouquet = relationship('Bouquet', back_populates='products')
    flower = relationship('Flower', back_populates='products')
    material = relationship('AdditionalMaterial', back_populates='products')
    order_details = relationship('OrderDetail', back_populates='product', lazy='dynamic')
    delivery_details = relationship('DeliveryDetail', back_populates='product', lazy='dynamic')


class Client(db.Model):
    __tablename__ = 'clients'

    client_id = db.Column('client_id', db.BigInteger, primary_key=True)
    full_name = db.Column('full_name', db.String(100))
    age = db.Column('age', db.Integer)
    phone_number = db.Column('phone_number', db.String(20))
    first_order_date = db.Column('first_order_date', db.Date)

    orders = relationship('Order', back_populates='client', lazy='dynamic')


class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column('order_id', db.BigInteger, primary_key=True)
    order_date = db.Column('order_date', db.Date)
    employee_id = db.Column(db.BigInteger, ForeignKey('employees.employee_id', ondelete='SET NULL'))
    client_id = db.Column(db.BigInteger, ForeignKey('clients.client_id', ondelete='CASCADE'))
    order_status = db.Column('order_status', db.String(50))

    order_details = relationship('OrderDetail', back_populates='order', lazy='dynamic')
    payments = relationship('Payment', back_populates='order', lazy='dynamic')
    employee = relationship('Employee', back_populates='orders')
    client = relationship('Client', back_populates='orders')


class OrderDetail(db.Model):
    __tablename__ = 'order_details'

    order_detail_id = db.Column('order_detail_id', db.BigInteger, primary_key=True)
    order_id = db.Column(db.BigInteger, ForeignKey('orders.order_id', ondelete='CASCADE'))
    product_id = db.Column(db.BigInteger, ForeignKey('products.product_id', ondelete='CASCADE'))
    quantity = db.Column('quantity', db.Integer)
    purchase_price = db.Column('purchase_price', db.Numeric(10, 2))

    order = relationship('Order', back_populates='order_details')
    product = relationship('Product', back_populates='order_details')


class Payment(db.Model):
    __tablename__ = 'payments'

    payment_id = db.Column('payment_id', db.BigInteger, primary_key=True)
    order_id = db.Column(db.BigInteger, ForeignKey('orders.order_id', ondelete='CASCADE'))
    payment_date = db.Column('payment_date', db.Date)
    amount = db.Column('amount', db.Numeric(10, 2))
    payment_method = db.Column('payment_method', db.String(50))

    order = relationship('Order', back_populates='payments')


class DeliveryDetail(db.Model):
    __tablename__ = 'delivery_details'

    delivery_detail_id = db.Column('delivery_detail_id', db.BigInteger, primary_key=True)
    delivery_id = db.Column(db.BigInteger, ForeignKey('deliveries.delivery_id', ondelete='CASCADE'))
    product_id = db.Column(db.BigInteger, ForeignKey('products.product_id', ondelete='CASCADE'))
    quantity = db.Column('quantity', db.Integer)
    purchase_price = db.Column('purchase_price', db.Numeric(10, 2))

    delivery = relationship('Delivery', back_populates='delivery_details')
    product = relationship('Product', back_populates='delivery_details')
