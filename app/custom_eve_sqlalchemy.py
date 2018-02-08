from eve_sqlalchemy import SQL
from eve_sqlalchemy.parser import parse_dictionary
from eve_sqlalchemy.utils import rename_relationship_fields_in_dict, sqla_object_to_dict
from sqlalchemy.sql.expression import func


class CUSTOM_SQL(SQL):

    def find_random_one(self, resource, req, **lookup):
        client_projection = self._client_projection(req)
        client_embedded = self._client_embedded(req)
        model, filter_, fields, _ = \
            self._datasource_ex(resource, [], client_projection, None,
                                client_embedded)

        lookup = rename_relationship_fields_in_dict(model, lookup)
        id_field = self._id_field(resource)
        if isinstance(lookup.get(id_field), dict) \
                or isinstance(lookup.get(id_field), list):
            # very dummy way to get the related object
            # that commes from embeddable parameter
            return lookup
        else:
            # filter_ = self.combine_queries(filter_,
            #                                parse_dictionary(lookup, model))

            query = self.driver.session.query(model)
            # db.session.query(Host).order_by(r).first()
            document = query.order_by(func.rand()).first()

        return sqla_object_to_dict(document, fields) if document else None

