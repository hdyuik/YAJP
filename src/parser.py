from .errors import *
# class Input:
#     def __init__(self, text):
#         self.text = text
#         self._length = len(text)
#         self._now = 0
#
#     def next(self):
#         if self._now >= self._length:
#             return '\0'
#         else:
#             char = self.text[self._now]
#             self._now += 1
#             return char


def reach_end(json, at):
    assert not at > len(json)
    return at == len(json)


def filter_space(json, at):
    while at < len(json) and json[at] in [' ', '\t', '\n', '\r']:
        at += 1
    return json, at


def parse_null(json, at):
    if json[at:at + 4] != 'null':
        raise InvalidInput(at)
    else:
        at += 4
        return None, at


def parse_true(json, at):
    if json[at:at + 4] != 'true':
        raise InvalidInput(at)
    else:
        at += 4
        return True, at


def parse_false(json, at):
    if json[at:at + 5] != 'false':
        raise InvalidInput(at)
    else:
        at += 5
        return False, at


def parse_number(json, at):
    assert not reach_end(json, at)
    dup = at
    if json[dup] == '-':
        dup += 1

    if (not reach_end(json, dup)) and json[dup] == '0':
        dup += 1
    elif (not reach_end(json, dup)) and (json[dup] in (str(i) for i in range(1, 10))):
        dup += 1
        while (not reach_end(json, dup)) and (json[dup] in (str(i) for i in range(0, 10))):
            dup += 1
    else:
        raise InvalidInput(dup)

    if (not reach_end(json, dup)) and json[dup] == '.':
        dup += 1
        if (not reach_end(json, dup)) and json[dup] in (str(i) for i in range(0, 10)):
            dup += 1
            while (not reach_end(json, dup)) and (json[dup] in (str(i) for i in range(0, 10))):
                dup += 1
        else:
            raise InvalidInput(dup)

    if (not reach_end(json, dup)) and (json[dup] in ('e', 'E')):
        dup += 1
        if json[dup] in ('-', '+'):
            dup += 1
        if (not reach_end(json, dup)) and json[dup] in (str(i) for i in range(0, 10)):
            dup += 1
            while (not reach_end(json, dup)) and json[dup] in (str(i) for i in range(0, 10)):
                dup += 1
        else:
            raise InvalidInput(dup)

    result = float(json[at:dup])
    return result, dup


def parse_string(json, at):
    assert (not reach_end(json, at)) and json[at] == '\"'
    at += 1
    s = ""
    while True:
        if reach_end(json, at):
            raise MissQuotationMark(at)
        elif json[at] == '"':
            at += 1
            return s, at
        elif json[at] == '\\':
            at += 1
            if json[at] == '\"':
                s += '\"'
                at += 1
            elif json[at] == '\\':
                s += '\\'
                at += 1
            elif json[at] == '/':
                s += '/'
                at += 1
            elif json[at] == 'b':
                s += '\b'
                at += 1
            elif json[at] == 'f':
                s += '\f'
                at += 1
            elif json[at] == 'n':
                s += '\n'
                at += 1
            elif json[at] == 'r':
                s += '\r'
                at += 1
            elif json[at] == 't':
                s += '\t'
                at += 1
            else:
                # utf-escape
                pass
        elif ord(json[at]) < 32:
            raise InvalidControlCharacter(at)
        else:
            s += json[at]
            at += 1


def parse_array(json, at):
    assert (not reach_end(json, at) and (json[at] == '['))
    at += 1
    ls = []
    if reach_end(json, at):
        raise MissBracketForArray(at)

    json, at = filter_space(json, at)
    if json[at] == ']':
        return ls
    while True:
        if reach_end(json, at):
            raise MissBracketForArray(at)

        json, at = filter_space(json, at)
        if reach_end(json, at):
            raise MissBracketForArray(at)

        item, at = parse_at(json, at)
        if reach_end(json, at):
            raise MissBracketForArray(at)

        ls.append(item)
        json, at = filter_space(json, at)
        if reach_end(json, at):
            raise MissBracketForArray(at)

        if json[at] == ']':
            at += 1
            return ls, at
        if json[at] == ',':
            at += 1


def parse_at(json, at):

    if json[at] == 'n':
        return parse_null(json, at)
    elif json[at] == 't':
        return parse_true(json, at)
    elif json[at] == 'f':
        return parse_false(json, at)
    elif json[at] == '\"':
        return parse_string(json, at)
    elif json[at] == '[':
        return parse_array(json, at)
    else:
        return parse_number(json, at)


def parse(json):
    json, at = filter_space(json, 0)

    if reach_end(json, at):
        raise NoInput

    result, at = parse_at(json, at)

    json, at = filter_space(json, at)

    if not reach_end(json, at):
        raise RootNotSingular(at)

    return result


def loads(json):
    assert type(json) is str
    return parse(json)
