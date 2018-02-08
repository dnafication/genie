# -*- coding: utf-8 -*-

"""
    customization of following library!!!

    eve.endpoints
    ~~~~~~~~~~~~~

    This module implements the API endpoints. Each endpoint (resource, item,
    home) invokes the appropriate method handler, returning its response
    to the client, properly rendered.

    :copyright: (c) 2016 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""

from bson import tz_util
from flask import abort, request, current_app as app, Response

from eve.auth import requires_auth, resource_auth
from eve.methods import get, getitem, post, patch, delete, deleteitem, put
from eve.methods.common import ratelimit
from eve.render import send_response
from eve.utils import config, weak_date, date_to_rfc1123
import eve
from eve.endpoints import _resource
import custom_get

@app.route('/random/<resource>')
def random_item_endpoint(resource, **lookup):
    """ Item endpoint handler

    :param url: the url that led here
    :param lookup: sub resource query
    """
    resource = resource
    response = None
    method = request.method
    if method in ('GET', 'HEAD'):
        response = custom_get.getitem(resource, **lookup)
    # elif method == 'PATCH':
    #     response = patch(resource, **lookup)
    # elif method == 'PUT':
    #     response = put(resource, **lookup)
    # elif method == 'DELETE':
    #     response = deleteitem(resource, **lookup)
    elif method == 'OPTIONS':
        send_response(resource, response)
    else:
        abort(405)
    return send_response(resource, response)
