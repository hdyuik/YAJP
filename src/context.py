class Context:
    def __init__(self, content):
        # pointer to the char that is already parsed
        self.content = content
        self.length = len(content)
        self.pointer = 0

    def __getitem__(self, offset):
        if type(offset) is int and self.pointer == self.length:
            return '\0'
        else:
            return self.content[offset]

    def look(self, forward=True):
        if forward:
            return self[self.pointer]
        else:
            return self[self.pointer-1]

    def move(self, forward=True):
        if forward:
            char = self[self.pointer]
            self.pointer += 1
            return char
        else:
            self.pointer -= 1
            return self[self.pointer]

    def accept(self, *char):
        if self.look() in char:
            self.move()
            return True
        else:
            return False

    def head(self):
        return self.pointer == -1

    def end(self):
        return self.pointer == self.length

    def error(self):
        msg = """Error When Parsing. At: line {0}, column {1}. """
        return msg.format(*self.position())

    def position(self):
        line = 1
        column = 0
        for offset, char in enumerate(self.content):
            if offset == self.pointer:
                column += 1
                break
            if char == '\n':
                line += 1
                column = 0
                continue
            column += 1
        return line, column
