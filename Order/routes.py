"""
API Endpoints

/api/order/           - GET
/api/order/all        - GET
/api/order/add-item   - POST
/api/order/checkout   - POST

"""

from flask import Blueprint, jsonify, request
from models import Order, OrderItem, db
import requests
from flask_bcrypt import Bcrypt
from werkzeug.security import check_password_hash
import hashlib


order_blueprint = Blueprint('order_api_routes', __name__, url_prefix="/api/order")

USER_API_URL = 'http://127.0.0.1:5001/api/user'


def get_user(api_key):
    headers = {
        'Authorization': api_key
    }

    response = requests.get(USER_API_URL, headers=headers)
    if response.status_code != 200:
        return {'message': 'Not Authorized'}

    user = response.json()
    return user


@order_blueprint.route('/', methods=['GET'])
def get_open_order():
    api_key = request.headers.get('Authorization')
    if not api_key:
        return jsonify({'message': 'Not logged in'}), 401
    response = get_user(api_key)
    user = response.get('result')
    if not user:
        return jsonify({'message': 'Not logged in'}), 401

    open_order = Order.query.filter_by(user_id=user['id'], is_open=1).first()
    if open_order:
        return jsonify({
            'result': open_order.serialize()
        }), 200
    else:
        return jsonify({'message': 'No open orders'})


@order_blueprint.route('/all', methods=['GET'])
def all_orders():
    orders = Order.query.all()
    result = [order.serialize() for order in orders]
    return jsonify(result), 200

@order_blueprint.route('/add-item', methods=['POST'])
def add_order_item():
    api_key = request.headers.get('Authorization')

    if not api_key:
        return jsonify({'message': 'Not logged in'}), 401

    response = get_user(api_key)
    if not response.get('result'):
        return jsonify({'message': 'Not logged in'}), 401

    user = response.get('result')

    sha256_api_key=hashlib.sha256(api_key.encode()).hexdigest()

    # if check_password_hash():
    #     return {'authenticated': True, 'result': user}
    # else:
    #     return {'authenticated': False, 'message': 'Invalid API key'}

    book_id = request.json.get('book_id')


    quantity = request.json.get('quantity')


    # # Check if book_id and quantity are provided
    # if book_id is None or quantity is None:
    #     return jsonify({'message': 'book_id and quantity are required'}), 400

    # # Convert book_id and quantity to integers
    # try:
    #     book_id = int(book_id)
    #     quantity = int(quantity)
    # except ValueError:
    #     return jsonify({'message': 'Invalid data type for book_id or quantity. They must be integers.'}), 400

    user_id = user['id']


    open_order = Order.query.filter_by(user_id=user_id, is_open=1).first()

    if not open_order:
        open_order = Order()
        open_order.is_open = True
        open_order.user_id = user_id

        order_item = OrderItem(book_id=book_id, quantity=quantity)
        open_order.order_items.append(order_item)
    else:
        found = False
        for item in open_order.order_items:
            if item.book_id == book_id:
                item.quantity += quantity
                found = True

        if not found:
            order_item = OrderItem(book_id=book_id, quantity=quantity)
            open_order.order_items.append(order_item)

    db.session.add(open_order)
    db.session.commit()

    return jsonify({"result": open_order.serialize()})



@order_blueprint.route('/checkout', methods=['POST'])
def checkout():
    api_key = request.headers.get('Authorization')
    if not api_key:
        return jsonify({'message': 'Not logged in'}), 401
    response = get_user(api_key)
    user = response.get('result')
    if not user:
        return jsonify({'message': 'Not logged in'}), 401

    open_order = Order.query.filter_by(user_id=user['id'], is_open=1).first()


    if open_order:
        open_order.is_open = False

        db.session.add(open_order)
        db.session.commit()
        return jsonify({'result': open_order.serialize()})
    else:
        return jsonify({'message': 'no open orders'})

