from flask import Flask, g, abort, request

# def create_app():
#     app = Flask(__name__)
#     with app.app_context():
#         print('Connecting to database and doing other setup stuff.')
#     return app

# app = create_app()

app = Flask(__name__)

products = [
    { 'id': '123', 'name': 'shoes', 'price': '$60.00'},
    { 'id': '234', 'name': 'socks', 'price': '$30.00'},
    { 'id': '345', 'name': 'jeans', 'price': '$100.00'},
    { 'id': '456', 'name': 'shirt', 'price': '$5.00'},
]

users = [
    { 'id': '123', 'name': 'dylan', 'cart': []},
    { 'id': '234', 'name': 'steve', 'cart': []},
]

@app.url_value_preprocessor
def get_product_id(endpoint, values):
    g.product_id = values.pop('product_id', None)
    g.user_id = values.pop('user_id', None)

@app.before_request
def before():
    if g.product_id:
        try:
            g.product = next(p for p in products if p['id'] == g.product_id)
        except StopIteration:
            abort(404)
    if g.user_id:
        try:
            g.user = next(u for u in users if u['id'] == g.user_id)
        except StopIteration:
            abort(404)

@app.get('/products/<string:product_id>')
def get_product_by_id():
    return g.product

@app.put('/products/<string:product_id>')
def update_product():
    update_fields = ['price']
    for field in update_fields:
        if field in request.json:
            new_value = request.json[field]
            g.product[field] = new_value

    return f'Updating product with id: {g.product["id"]}'

@app.put('/users/<string:user_id>/cart/<string:product_id>')
def add_to_cart():
    g.user['cart'].append(g.product)
    return f'Adding product with id {g.product["id"]} to user {g.user_id}. {g.user["cart"]}'

@app.after_request
def after(response):
    return response
