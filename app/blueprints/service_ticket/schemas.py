from marshmallow import fields

from app.extensions import ma
from app.models import ServiceTicket
from app.blueprints.mechanic.schemas import MechanicSchema


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = ma.Nested(MechanicSchema, many=True, dump_only=True)

    class Meta:
        model = ServiceTicket
        include_fk = True
        load_instance = False
        
class EditTicketSchema(ma.Schema):
    add_ids = fields.List(fields.Int(), required=True)
    remove_ids = fields.List(fields.Int(), required=True)
    class Meta:
        fields = ("add_ids", "remove_ids")


service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
edit_ticket_schema = EditTicketSchema()