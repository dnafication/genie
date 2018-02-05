"""
    Genie

    A simple REST API for test data management powered by Eve REST API.
    Features (Current & To Do):
      - Serve test data through various HTTP methods
      - REST-compliant API implementation. (can render XML & JSON response)
      - APIs can support the full range of CRUD operations.
      - etag is used for concurrency control and conditional requests.
      - Query strings are supported, allowing for filtering and sorting.
      - Hypermedia as the Engine of Application State (HATEOAS) is enabled by default.
      - TODO Custom methods/routes to access data
      - TODO Test data admin/bulk inserts
"""

from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL

from app.data_model.domain import Base, Host
from sqlalchemy.sql.expression import func
from flask import make_response

app = Eve(validator=ValidatorSQL, data=SQL)

# bind SQLAlchemy
db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base

# create database schema
db.create_all()
db.session.commit()


@app.route('/random/<resource>')
def random_resource_single(resource):
    """
    custom route to get a random value from db

    :param resource:
    :return:
    """
    if resource == 'hosts':
        r = func.rand()
        host = db.session.query(Host).order_by(r).first()
        resp = make_response("{} - {}".format(r, host.instance), 200)
        return resp
    else:
        return 'works only for hosts'


@app.route('/unique/<resource>')
def unique_resource_single(resource):
    """
    custom route to get a unique value from db (burn after read)
    consider using a header and a hook. basically use header which says whether the user need unique/random and also
    the count
    """
    pass


def pre_get_callback(resource, request, lookup):
    print('a get request was received on {}, request: {}, lookup: {}'.format(resource, request, lookup))

def callback_for_partnerships(request, lookup):
    print('this is for partnerships {}\n{}'.format(request, lookup))


app.on_pre_GET += pre_get_callback
app.on_pre_GET_partnerships += callback_for_partnerships

# using reloader will destroy the in-memory sqlite db
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
