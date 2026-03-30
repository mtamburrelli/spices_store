from app import create_app, db
from app.models import Product

app = create_app()

with app.app_context():

    # limpiar productos (opcional)
    Product.query.delete()

    # crear productos
    productos = [
        Product(name="Lentejas", price=1.50),
        Product(name="Arroz", price=0.90),
        Product(name="Frijoles", price=1.20),
        Product(name="Pimienta Negra", price=2.75),
        Product(name="Canela", price=3.10),
    ]

    # guardar en DB
    db.session.add_all(productos)
    db.session.commit()

    print("Productos insertados ✅")