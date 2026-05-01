from .schemas import customer_schema, customers_schema, login_schema
from flask import jsonify, request
from app.models import Customer, db
from marshmallow import ValidationError
from sqlalchemy import select
from . import customers_bp
from app.extensions import limiter
from app.utils.util import encode_token, token_required


# LOGIN CUSTOMER
@customers_bp.route("/login", methods=["POST"])
def login():
    try:
        credentials = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    username = credentials["email"]
    password = credentials["password"]

    query = select(Customer).where(Customer.email == username)
    user = db.session.execute(query).scalar_one_or_none()

    if user and user.password == password:
        auth_token = encode_token(user.id)

        return jsonify({
            "status": "success",
            "message": "Successfully Logged In",
            "auth_token": auth_token
        }), 200

    return jsonify({"message": "Invalid email or password"}), 401


# CREATE CUSTOMER
@customers_bp.route("/", methods=["POST"])
@limiter.limit("20 per hour")
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Customer).where(Customer.email == customer_data["email"])
    existing_customer = db.session.execute(query).scalars().first()

    if existing_customer:
        return jsonify({"error": "Email already associated with an account."}), 400

    new_customer = Customer(
        name=customer_data["name"],
        email=customer_data["email"],
        phone_number=customer_data["phone_number"],
        password=customer_data["password"]
    )

    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 201


# GET ALL CUSTOMERS WITH PAGINATION
@customers_bp.route("/", methods=["GET"])
def get_customers():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    query = select(Customer)

    pagination = db.paginate(
        query,
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "customers": customers_schema.dump(pagination.items),
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev
    }), 200


# GET CUSTOMER BY ID
@customers_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    return customer_schema.jsonify(customer), 200


# UPDATE CUSTOMER
@customers_bp.route("/<int:customer_id>", methods=["PUT"])
@token_required
def update_customer(user_id, customer_id):
    
    if user_id != customer_id:
        return jsonify({
        "error": "Unauthorized",
        "message": "You can only modify your own account"
        }), 403

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


# DELETE LOGGED-IN CUSTOMER
@customers_bp.route("/", methods=["DELETE"])
@token_required
def delete_user(user_id):
    query = select(Customer).where(Customer.id == user_id)
    user = db.session.execute(query).scalars().first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": f"Successfully deleted user {user_id}"}), 200