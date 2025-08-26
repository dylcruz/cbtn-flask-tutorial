import json
from flask import Flask, g, make_response, request

app = Flask(__name__)

products = [
    {"id": "1", "name": "Shoes", "price": "$40.00"},
    {"id": "2", "name": "Shirt", "price": "$20.00"},
    {"id": "3", "name": "Pants", "price": "$30.00"},
    {"id": "4", "name": "Hat", "price": "$10.00"},
]


@app.before_request
def parse_cart():
    cart_cookie_value = request.cookies.get("cart")
    cart_ids = json.loads(cart_cookie_value)
    g.cart_ids = cart_ids


@app.get("/cart")
def load_user_cart():
    cart_items = [
        next(product for product in products if product["id"] == id)
        for id in g.cart_ids
    ]
    return cart_items


@app.put("/cart")
def add_to_cart():
    item_id_to_add = request.json["id"]
    g.cart_ids.append(item_id_to_add)
    return "Successfully added item to cart!"


@app.delete("/cart/<string:item_id>")
def delete_from_cart(item_id):
    remove_item_id = next(id for id in g.cart_ids if id == item_id)
    g.cart_ids.remove(remove_item_id)
    return "Successfuly removed item from cart!"


@app.delete("/cart/clear")
def clear_cart():
    g.cart_ids = []
    return "Successfully cleared the cart!"


@app.after_request
def update_cart_cookie(response):
    response.set_cookie("cart", json.dumps(g.cart_ids))
    return response
