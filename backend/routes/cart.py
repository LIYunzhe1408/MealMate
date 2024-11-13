from flask import Blueprint, request, jsonify

cart_bp = Blueprint('cart', __name__)

# In-memory cart storage (replace with database in production)
shopping_carts = {}

@cart_bp.route('/cart', methods=['GET'])
def get_cart():
    cart_id = request.args.get('cart_id')
    return jsonify(shopping_carts.get(cart_id, {'items': []}))

@cart_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.json
    cart_id = data.get('cart_id')
    item = data.get('item')
    
    if cart_id not in shopping_carts:
        shopping_carts[cart_id] = {'items': []}
    
    shopping_carts[cart_id]['items'].append(item)
    return jsonify(shopping_carts[cart_id])