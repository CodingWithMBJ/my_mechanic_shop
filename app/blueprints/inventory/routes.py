from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select

from app.models import Inventory, db
from . import inventory_bp
from .schemas import inventory_schema, inventories_schema


# CREATE INVENTORY PART
@inventory_bp.route("/", methods=["POST"])
def create_inventory():
    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_part = Inventory(**inventory_data)

    db.session.add(new_part)
    db.session.commit()

    return inventory_schema.jsonify(new_part), 201


# GET ALL INVENTORY PARTS
@inventory_bp.route("/", methods=["GET"])
def get_inventory():
    query = select(Inventory)
    parts = db.session.execute(query).scalars().all()

    return inventories_schema.jsonify(parts), 200


# GET INVENTORY PART BY ID
@inventory_bp.route("/<int:inventory_id>", methods=["GET"])
def get_inventory_part(inventory_id):
    part = db.session.get(Inventory, inventory_id)

    if not part:
        return jsonify({"error": "Inventory part not found."}), 404

    return inventory_schema.jsonify(part), 200


# UPDATE INVENTORY PART
@inventory_bp.route("/<int:inventory_id>", methods=["PUT"])
def update_inventory(inventory_id):
    part = db.session.get(Inventory, inventory_id)

    if not part:
        return jsonify({"error": "Inventory part not found."}), 404

    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in inventory_data.items():
        setattr(part, key, value)

    db.session.commit()

    return inventory_schema.jsonify(part), 200


# DELETE INVENTORY PART
@inventory_bp.route("/<int:inventory_id>", methods=["DELETE"])
def delete_inventory(inventory_id):
    part = db.session.get(Inventory, inventory_id)

    if not part:
        return jsonify({"error": "Inventory part not found."}), 404

    db.session.delete(part)
    db.session.commit()

    return jsonify({
        "message": f"Inventory part id: {inventory_id}, successfully deleted."
    }), 200