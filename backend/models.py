from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Interval, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    region = Column(String, nullable=True)
    services = relationship('Service', back_populates='department')

class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    mandated_days = Column(Integer, nullable=False)  # e.g., 7 days for birth certificate
    department_id = Column(Integer, ForeignKey('departments.id'))
    department = relationship('Department', back_populates='services')
    requests = relationship('Request', back_populates='service')

class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True)
    citizen_name = Column(String, nullable=False)
    request_date = Column(Date, nullable=False)
    delivery_id = Column(Integer, ForeignKey('deliveries.id'))
    service_id = Column(Integer, ForeignKey('services.id'))
    service = relationship('Service', back_populates='requests')
    delivery = relationship('Delivery', back_populates='request', uselist=False)

class Delivery(Base):
    __tablename__ = 'deliveries'
    id = Column(Integer, primary_key=True)
    delivered_date = Column(Date, nullable=False)
    is_late = Column(Boolean, default=False)
    request = relationship('Request', back_populates='delivery', uselist=False)
