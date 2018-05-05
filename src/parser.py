from .context import Context
from .errors import *
DIGIT = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
DIGIT_1_9 = ['1', '2', '3', '4', '5', '6', '7', '8', '9']


def filter_space(context):
    while context.accept(' ', '\r', '\n', '\t'):
        pass


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
    func = d.get(context.peek(), None)
    if func is None:
        raise InvalidInput(context.pointer)
    else:
        context.forward()
        return func(context)


def parse_unicode(context):
    raise NotImplementedError()


def parse_array(context):
    ls = []
    filter_space(context)
    if context.accept(']'):
        return ls
    while True:
        if context.end():
            raise MissBracketForArray(context.pointer)
        item = parse_at(context)
        filter_space(context)
        ls.append(item)
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

        if not context.accept('\"'):
            raise InvalidInput(context.pointer)
        key = parse_string(context)
        filter_space(context)

        if not context.accept(':'):
            raise NoColonAfterKey(context.pointer)
        filter_space(context)

        value = parse_at(context)
        filter_space(context)

        obj[key] = value

        if context.accept('}'):
            return obj
        elif context.accept(','):
            filter_space(context)
        else:
            raise MissComma(context.pointer)


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
