import json
from flask import Flask, g, request, render_template

app = Flask(__name__)

products = [
    {"id": "1", "name": "Shoes", "price": "$40.00"},
    {"id": "2", "name": "Shirt", "price": "$20.00"},
    {"id": "3", "name": "Pants", "price": "$30.00"},
    {"id": "4", "name": "Hat", "price": "$10.00"},
]


@app.before_request
def parse_cart():
    cart_cookie_value = request.cookies.get("cart") or '[]'
    cart_ids = json.loads(cart_cookie_value)
    g.cart_ids = cart_ids


@app.get('/products')
def products_page():
    products_with_added_data = [{**product, 'isInCart': product.get('id') in g.cart_ids}  for product in products]
    return render_template('products.html', products=products_with_added_data)


@app.get('/cart')
def cart_page():
    cart_items = [
        next(product for product in products if product["id"] == id)
        for id in g.cart_ids
    ]
    return render_template(
        'shopping-cart.html', 
        products=cart_items, 
        cartIsEmpty=len(cart_items) == 0
        )


@app.get("/api/cart")
def load_user_cart():
    cart_items = [
        next(product for product in products if product["id"] == id)
        for id in g.cart_ids
    ]
    return cart_items


@app.put("/api/cart")
def add_to_cart():
    item_id_to_add = request.json["id"]
    g.cart_ids.append(item_id_to_add)
    return {"message": "Successfully added item to cart!" }


@app.delete("/api/cart/<string:item_id>")
def delete_from_cart(item_id):
    remove_item_id = next(id for id in g.cart_ids if id == item_id)
    g.cart_ids.remove(remove_item_id)
    return "Successfuly removed item from cart!"


@app.delete("/api/cart/clear")
def clear_cart():
    g.cart_ids = []
    return "Successfully cleared the cart!"


@app.after_request
def update_cart_cookie(response):
    response.set_cookie("cart", json.dumps(g.cart_ids))
    return response
