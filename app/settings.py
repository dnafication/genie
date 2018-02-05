"""
    Genie - settings

    This sets up the settings for EVE and SQLAlchemy and creates the domain.
"""
from eve_sqlalchemy.config import DomainConfig, ResourceConfig

from app.data_model.domain import Host, Partnership, Address, Appointment, Order

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:example@localhost:3306/genie'

SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST']

# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

# The following two lines will output the SQL statements executed by
# SQLAlchemy. This is useful while debugging and in development, but is turned
# off by default.
# --------
# SQLALCHEMY_ECHO = True
# SQLALCHEMY_RECORD_QUERIES = True

# The default schema is generated using DomainConfig:
DOMAIN = DomainConfig({
    'hosts': ResourceConfig(Host),
    'partnerships': ResourceConfig(Partnership),
    'addresses': ResourceConfig(Address),
    'appointments': ResourceConfig(Appointment),
    'orders': ResourceConfig(Order)
}).render()
