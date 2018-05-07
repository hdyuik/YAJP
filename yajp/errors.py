class DecodeError(Exception):
    def __init__(self, context, description=None):
        line, column = context.position()
        self.line = line
        self.column = column
        self.description = description
        errmsg = "{0}: At line {1} column {2}".format(description, line, column)
        Exception.__init__(self, errmsg)

