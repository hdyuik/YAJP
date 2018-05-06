from .context import Context
from .errors import *
DIGIT = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
DIGIT_1_9 = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
HEX = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
       'A', 'B', 'C', 'D', 'E', 'F',
       'a', 'b', 'c', 'd', 'e', 'f']


def filter_space(context):
    while context.accept(' ', '\r', '\n', '\t'):
        pass


# literal
def match_literal(context, string):
    for char in string:
        if not context.accept(char):
            raise InvalidInput(context.pointer)
    return True


def parse_null(context):
    if match_literal(context, 'ull'):
        return None


def parse_true(context):
    if match_literal(context, 'rue'):
        return True


def parse_false(context):
    if match_literal(context, 'alse'):
        return False


# number
def parse_number(context):
    i = context.pointer
    context.pointer -= 1

    context.accept('-')

    if context.accept('0'):
        pass
    elif context.accept(*DIGIT_1_9):
        while context.accept(*DIGIT):
            pass
    else:
        raise InvalidInput(context.pointer)

    if context.accept('.'):
        if context.accept(*DIGIT):
            while context.accept(*DIGIT):
                pass
        else:
            raise InvalidInput(context.pointer)

    if context.accept('e', 'E'):
        context.accept('+', '-')
        if context.accept(*DIGIT):
            while context.accept(*DIGIT):
                ...
        else:
            raise InvalidInput(context.pointer)

    return float(context[i:context.pointer+1])


# string
def parse_string(context):
    s = ""

    while True:
        if context.end():
            raise MissQuotationMark(context.pointer)
        elif context.accept('\"'):
            return s
        elif context.accept('\\'):
            s += parse_escape(context)
        elif ord(context.peek()) < 32:
            raise InvalidControlCharacter(context.pointer)
        else:
            s += context.forward()


def parse_escape(context):
    d = {
        '\"': lambda ctx: '\"',
        '\\': lambda ctx: '\\',
        '/': lambda ctx: '/',
        'b': lambda ctx: '\b',
        'f': lambda ctx: '\f',
        'n': lambda ctx: '\n',
        'r': lambda ctx: '\r',
        't': lambda ctx: '\t',
        'u': parse_unicode,
    }
    func = d.get(context.forward(), None)
    if func is None:
        raise InvalidInput(context.pointer)
    else:
        return func(context)


def parse_unicode(context):
    codepoint = parse_codepoint(context)
    if codepoint < 32:
        raise InvalidControlCharacter(context.pointer)
    return chr(codepoint)


def parse_codepoint(context, low_surrogate=False):
    s = ""
    for i in range(4):
        if context.peek() in HEX:
            s += context.forward()
        else:
            raise InvalidInput(context.pointer)
    codepoint = int('0x' + s, 16)
    if low_surrogate:
        if not(0xDC00 <= codepoint <= 0xDFFF):
            raise InvalidUnicodeSurrogate(context.pointer)
        else:
            return codepoint
    else:
        if 0xD800 <= codepoint <= 0xDBFF:
            if not (context.accept('\\') and context.accept('u')):
                raise InvalidUnicodeSurrogate(context.pointer)
            return 0x10000 + (codepoint - 0xD800) * 0x400 + (parse_codepoint(context, low_surrogate=True) - 0xDC00)
        else:
            return codepoint


# compound
def parse_array(context):
    ls = []
    filter_space(context)
    if context.accept(']'):
        return ls
    while True:
        if context.end():
            raise MissBracketForArray(context.pointer)

        value = parse_value(context)
        ls.append(value)

        if context.accept(']'):
            return ls
        elif context.accept(','):
            filter_space(context)
        else:
            raise MissComma(context.pointer)


def parse_obj(context):
    obj = {}
    filter_space(context)
    if context.accept('}'):
        return obj
    while True:
        if context.end():
            raise MissBraceForObj(context.pointer)

        key = parse_key(context)

        if not context.accept(':'):
            raise NoColonAfterKey(context.pointer)
        filter_space(context)

        value = parse_value(context)

        obj[key] = value

        if context.accept('}'):
            return obj
        elif context.accept(','):
            filter_space(context)
        else:
            raise MissComma(context.pointer)


def parse_key(context):
    if not context.accept('\"'):
        raise InvalidInput(context.pointer)
    key = parse_string(context)
    filter_space(context)
    return key


def parse_value(context):
    value = parse_at(context)
    filter_space(context)
    return value


# entry
def parse_at(context):
    d = {
        'n': parse_null,
        't': parse_true,
        'f': parse_false,
        '\"': parse_string,
        '[': parse_array,
        '{': parse_obj,
    }
    default = parse_number
    func = d.get(context.forward(), default)
    return func(context)


def parse(json):
    context = Context(json)
    filter_space(context)

    if context.end():
        raise NoInput(context.pointer)

    result = parse_at(context)

    filter_space(context)

    if context.end():
        return result
    else:
        raise RootNotSingular(context.pointer)


def loads(json):
    assert type(json) is str
    return parse(json)
