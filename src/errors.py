class ParseError(Exception):
    def __init__(self, context, detail=None):
        self.shit = 1
        self.context = context
        self.detail = detail

    def position(self):
        line = 1
        column = 0
        for offset, char in enumerate(self.context.content):
            if offset == self.context.pointer:
                column += 1
                break
            if char == '\n':
                line += 1
                column = 0
                continue
            column += 1
        return line, column
