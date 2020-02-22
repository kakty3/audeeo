class RestResult(object):
    def __init__(self, data, schema, total=None):
        self.data = data
        self.schema = schema
        self.total = total
