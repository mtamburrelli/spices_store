from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)  # nombre persona o empresa
    email = db.Column(db.String(150))
    phone = db.Column(db.String(50))

    address = db.Column(db.String(200), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    status = db.Column(db.String(50), default='pending')
    total = db.Column(db.Float)


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    quantity = db.Column(db.Integer)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    method = db.Column(db.String(50))  # Yappy o ACH
    receipt = db.Column(db.String(200))  # imagen comprobante
    status = db.Column(db.String(50), default='pending')
