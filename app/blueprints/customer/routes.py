from .schemas import customer_schema, customers_schema, login_schema
from flask import jsonify, request
from app.models import Customer, db
from marshmallow import ValidationError
from sqlalchemy import select
from . import customers_bp
from app.extensions import limiter, cache
from app.utils.util import encode_token, token_required




#=========> CRUD Endpoints <==========#


#LOGIN function

@customers_bp.route('/login', methods=['POST'])
def login():
    try:
        credentials = request.json
        username = credentials['email']
        password = credentials['password']
    except KeyError:
        return jsonify -({'messages': 'Invalid payload, expecting username and password'}), 400
    
    query =select(Customer).where(Customer.email == username)
    user = db.session.execute(query).scalar_one_or_none() #Query user table for a user with this email
    
    if user and user.password == password: #if we have a user associated with the username, validate the password
        auth_token = encode_token(user.id)
        
        response = {
            "status": "success",
            "message": "Successfully Logged In",
            "auth_token": auth_token
        }
        return jsonify(response), 200
    else:
        return jsonify({'messages': "Invalid email or password"}), 401
    


# CREATE CUSTOMER

@customers_bp.route("/", methods=['POST'])
@limiter.limit("3 per hour") #A client can only attempt to make 3 customers per hour
def create_customer():
    try: 
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == customer_data['email'])
    existing_customer = db.session.execute(query).scalars().all()
    if existing_customer:
        return jsonify({"error": "Email already associated with an account."}), 400
    
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone_number=customer_data['phone_number'], password=customer_data['password'])
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

# GET ALL CUSTOMERS

@customers_bp.route("/", methods=['GET'])
@cache.cached(timeout=60)
def get_customers():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    
    return customers_schema.jsonify(customers)



# GET CUSTOMER BY ID


@customers_bp.route("/<int:customer_id>", methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    
    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"error": "Customer not found."}), 400


# UPDATE CUSTOMERS

@customers_bp.route("/<int:customer_id>", methods=['PUT'])
@token_required
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in customer_data.items():
        setattr(customer, key, value)
        
    db.session.commit()
    return customer_schema.jsonify(customer), 200


# DELETE CUSTOMER

# @customers_bp.route("/<int:customer_id>", methods=['DELETE'])
# def delete_customer(customer_id):
#     customer = db.session.get(Customer, customer_id)
    
#     if not customer:
#         return jsonify({"error": "Customer not found"}), 404
    
#     db.session.delete(customer)
#     db.session.commit()
#     return jsonify({"message": f'Customer id: {customer_id}, successfully deleted.'}), 200


@customers_bp.route('/', methods=['DELETE'])
@token_required
def delete_user(user_id):
    query = select(Customer).where(Customer.id == user_id)
    user = db.session.execute(query).scalars().first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": f"successfully deleted user {user_id}"}), 200
                