from app.utils.util import token_required

from .schemas import service_ticket_schema, service_tickets_schema, edit_ticket_schema
from flask import jsonify, request
from app.models import ServiceTicket, Mechanic, db, Inventory
from marshmallow import ValidationError
from sqlalchemy import select
from . import service_ticket_bp


# CREATE SERVICE TICKET
@service_ticket_bp.route("/", methods=["POST"])
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_service_ticket = ServiceTicket(**service_ticket_data)

    db.session.add(new_service_ticket)
    db.session.commit()

    return service_ticket_schema.jsonify(new_service_ticket), 201


# GET ALL SERVICE TICKETS
@service_ticket_bp.route("/", methods=["GET"])
@token_required
def get_service_tickets(user_id):
    query = select(ServiceTicket)
    service_tickets = db.session.execute(query).scalars().all()

    return service_tickets_schema.jsonify(service_tickets), 200


# ASSIGN MECHANIC TO SERVICE TICKET
@service_ticket_bp.route(
    "/<int:ticket_id>/assign-mechanic/<int:mechanic_id>",
    methods=["PUT"]
)
def assign_mechanic(ticket_id, mechanic_id):
    service_ticket = db.session.get(ServiceTicket, ticket_id)

    if not service_ticket:
        return jsonify({"error": "Service Ticket not found."}), 404

    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    if mechanic in service_ticket.mechanics:
        return jsonify({"error": "Mechanic already assigned to this ticket."}), 400

    service_ticket.mechanics.append(mechanic)
    db.session.commit()

    return service_ticket_schema.jsonify(service_ticket), 200


# REMOVE MECHANIC FROM SERVICE TICKET
@service_ticket_bp.route(
    "/<int:ticket_id>/remove-mechanic/<int:mechanic_id>",
    methods=["PUT"]
)
def remove_mechanic(ticket_id, mechanic_id):
    service_ticket = db.session.get(ServiceTicket, ticket_id)

    if not service_ticket:
        return jsonify({"error": "Service Ticket not found."}), 404

    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404

    if mechanic not in service_ticket.mechanics:
        return jsonify({"error": "Mechanic is not assigned to this ticket."}), 400

    service_ticket.mechanics.remove(mechanic)
    db.session.commit()

    return service_ticket_schema.jsonify(service_ticket), 200


@service_ticket_bp.route("/<int:ticket_id>/edit", methods=["PUT"])
@token_required
def edit_ticket_mechanics(user_id, ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    try:
        data = edit_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    add_ids = data.get("add_ids", [])
    remove_ids = data.get("remove_ids", [])

    for mechanic_id in add_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)

        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)

    for mechanic_id in remove_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)

        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)

    db.session.commit()

    return jsonify({
        "message": "Mechanics updated successfully",
        "ticket": service_ticket_schema.dump(ticket)
    }), 200
    
    
    
@service_ticket_bp.route("/my-tickets", methods=["GET"])
@token_required
def get_my_tickets(user_id):
    query = select(ServiceTicket).where(ServiceTicket.customer_id == user_id)
    tickets = db.session.execute(query).scalars().all()

    return service_tickets_schema.jsonify(tickets), 200


@service_ticket_bp.route("/<int:ticket_id>/add-part/<int:part_id>", methods=["PUT"])
@token_required
def add_part_to_ticket(user_id, ticket_id, part_id):
    ticket = db.session.get(ServiceTicket, ticket_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404


    if ticket.customer_id != int(user_id):
        return jsonify({"error": "Unauthorized"}), 403

    part = db.session.get(Inventory, part_id)

    if not part:
        return jsonify({"error": "Part not found"}), 404

    if part in ticket.parts:
        return jsonify({"error": "Part already added to this ticket"}), 400

    ticket.parts.append(part)
    db.session.commit()

    return jsonify({
        "message": "Part added successfully",
        "ticket": service_ticket_schema.dump(ticket)
    }), 200