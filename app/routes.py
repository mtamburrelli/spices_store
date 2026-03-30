from collections import Counter
import os
from flask import Blueprint, jsonify, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename
from .models import Product

main = Blueprint('main', __name__)


def _cart_lines_and_total():
    cart_ids = session.get('cart', [])
    if not cart_ids:
        return [], 0.0
    counts = Counter(cart_ids)
    lines = []
    total = 0.0
    for pid, qty in sorted(counts.items()):
        product = Product.query.get(pid)
        if not product:
            continue
        line_total = product.price * qty
        total += line_total
        lines.append(
            {"product": product, "quantity": qty, "line_total": line_total}
        )
    return lines, total


@main.route('/')
def home():
    return render_template('spa.html')


@main.route('/api/products')
def api_products():
    products = Product.query.order_by(Product.id).all()
    return jsonify(
        [
            {
                "id": p.id,
                "name": p.name,
                "price": float(p.price),
            }
            for p in products
        ]
    )


@main.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    cart = session.get('cart', [])
    cart.append(id)
    session['cart'] = cart
    return redirect('/')


@main.route('/remove_from_cart/<int:id>', methods=['POST'])
def remove_from_cart(id):
    """Quita 1 unidad del producto del carrito."""
    cart = session.get('cart', [])
    try:
        cart.remove(id)  # quita 1 unidad
    except ValueError:
        pass

    if cart:
        session['cart'] = cart
    else:
        session.pop('cart', None)

    return redirect(url_for('main.checkout'))


@main.route('/clear_cart', methods=['POST'])
def clear_cart():
    """Limpia el carrito cuando se cierra la pestaña/navegación externa."""
    session.pop('cart', None)
    return ('', 204)


@main.route('/checkout')
def checkout():
    return render_template('spa.html')


@main.route('/upload', methods=['POST'])
def upload():
    method = request.form.get('payment_method')
    if method not in ('ach', 'yappy'):
        return redirect(url_for('main.checkout'))

    receipt = request.files.get('receipt')
    if not receipt or not receipt.filename:
        return redirect(url_for('main.checkout'))

    safe_name = secure_filename(receipt.filename)
    if not safe_name:
        return redirect(url_for('main.checkout'))

    upload_dir = os.path.join(
        os.path.dirname(__file__), 'static', 'uploads'
    )
    os.makedirs(upload_dir, exist_ok=True)
    path = os.path.join(upload_dir, safe_name)
    receipt.save(path)

    # una vez completado el checkout, limpiamos el carrito
    session.pop('cart', None)
    return "Uploaded"
