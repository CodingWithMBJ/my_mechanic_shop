from datetime import date
from typing import List

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Date, Float, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass
 


db = SQLAlchemy(model_class=Base)



service_mechanics = db.Table(
    'service_mechanics',
    Base.metadata,
    db.Column('ticket_id', ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('mechanic_id', ForeignKey('mechanics.id'), primary_key=True)
)


class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(360), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    service_tickets: Mapped[List['ServiceTicket']] = relationship(back_populates='customer')


class ServiceTicket(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(String(17), nullable=False, unique=True)
    service_date: Mapped[date] = mapped_column(Date, default=date.today)
    service_desc: Mapped[str] = mapped_column(String(200), nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable=False)

    customer: Mapped['Customer'] = relationship(back_populates='service_tickets')
    mechanics: Mapped[List['Mechanic']] = relationship(
        secondary=service_mechanics,
        back_populates='service_tickets'
    )


class Mechanic(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    salary: Mapped[float] = mapped_column(Float, nullable=False)

    service_tickets: Mapped[List['ServiceTicket']] = relationship(
        secondary=service_mechanics,
        back_populates='mechanics'
    )
