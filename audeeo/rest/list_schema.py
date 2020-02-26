from marshmallow import Schema, fields


def create_listresponse_schema(nested_schema):
    return type('ListResponseSchema', (Schema, ), {
        'total': fields.Integer(),
        'items': fields.List(
            fields.Nested(nested_schema)
        )
    })
