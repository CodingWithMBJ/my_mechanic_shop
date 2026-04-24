from .schemas import service_ticket_schema, service_tickets_schema
from flask import jsonify, request
from app.models import ServiceTicket, Mechanic, db
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
def get_service_tickets():
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