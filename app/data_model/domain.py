from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property, relationship

Base = declarative_base()


class CommonColumns(Base):
    __abstract__ = True
    _created = Column(DateTime, default=func.now())
    _updated = Column(DateTime, default=func.now(), onupdate=func.now())
    _etag = Column(String(40))


class Host(CommonColumns):
    __tablename__ = 'host'
    cpa_id = Column(String(30), primary_key=True)
    host = Column(String(45))
    port = Column(Integer)
    instance = Column(String(20))
    status = Column(String(10))
    partnerships = relationship("Partnership", back_populates='host')


class Partnership(CommonColumns):
    __tablename__ = 'partnership'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cpa_id = Column(String(30), ForeignKey('host.cpa_id'))
    service = Column(String(40))
    action = Column(String(50))
    fromPartyId = Column(String(30))
    fromPartyType = Column(String(20))
    fromPartyRole = Column(String(20))
    toPartyId = Column(String(30))
    toPartyType = Column(String(20))
    toPartyRole = Column(String(20))
    serviceType = Column(String(10))
    status = Column(String(10))
    host = relationship("Host", back_populates='partnerships')


class Address(CommonColumns):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, autoincrement=True)
    location_id = Column(String(30), unique=True)
    serviceability_class = Column(String(30))
    cpi_id = Column(String(30))
    t_cpi_id = Column(String(30))
    csa_id = Column(String(30))
    tech_type = Column(String(10))
    boundary = Column(String(30))
    olt_id = Column(String(30))
    dslam_logical_id = Column(String(30))
    cmts_logical_id = Column(String(30))
    dpu_physical_id = Column(String(30))
    dpu_logical_id = Column(String(30))
    dpu_serial_number = Column(String(30))
    shortfall = Column(String(30))
    sam_id = Column(String(30))
    ada = Column(String(30))


class Appointment(CommonColumns):
    __tablename__ = 'appointment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(30))
    appointment_id = Column(String(30), unique=True)
    location_id = Column(String(30), ForeignKey('address.location_id'))
    appointment_type = Column(String(30))
    cvc_id = Column(String(30))
    access_seeker = Column(String(30))
    address = relationship('Address')


class Order(CommonColumns):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String(30))
    order_status = Column(String(30))
    order_type = Column(String(30))
    product_id = Column(String(30))
    appointment_id = Column(String(30), ForeignKey('appointment.appointment_id'))
    location_id = Column(String(30), ForeignKey('address.location_id'))
    access_seeker = Column(String(30))


class Product(CommonColumns):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String(30))
    location_id = Column(String(30), ForeignKey('address.location_id'))
    bandwidth_profile = Column(String(30))
    template_id = Column(String(30))
    template_version = Column(String(30))
    ntd_id = Column(String(30))
    avc_id = Column(String(30))




