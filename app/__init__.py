from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'supersecret'
    # Queremos que el carrito no persista indefinidamente: por defecto Flask usa
    # cookies de sesión (se borran al cerrar el navegador).
    app.config['SESSION_PERMANENT'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)

    from . import models  # noqa: F401

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()
        from .models import Product
        if Product.query.count() == 0:
            db.session.add_all(
                [
                    Product(name="Comino molido", price=4.50),
                    Product(name="Pimentón ahumado", price=5.25),
                    Product(name="Cúrcuma en polvo", price=6.00),
                ]
            )
            db.session.commit()

    return app
