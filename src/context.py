class Context:
    def __init__(self, content):
        # pointer to the char that is already parsed
        assert type(content) is str
        self.content = content
        self.length = len(content)
        self.pointer = -1

    def __getitem__(self, index):
        if type(index) is slice:
            assert not index.stop > self.length, 'slice out of index'
        else:
            assert not index > self.length, 'offset out of index'
        if index == self.length:
            return '\0'
        else:
            return self.content[index]

    def peek(self):
        assert self.pointer < self.length, 'next out of index'
        return self[self.pointer+1]

    def current(self):
        assert self.pointer < self.length, 'current out of index'
        assert self.pointer != -1, 'not start '
        return self[self.pointer]

    def forward(self):
        self.pointer += 1
        assert self.pointer < self.length, 'forward out of index'
        return self[self.pointer]

    def accept(self, *char):
        if self.peek() in char:
            self.forward()
            return True
        else:
            return False

    def end(self):
        return self.peek() == '\0'
