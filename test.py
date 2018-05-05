from src.context import Context
from src.parser import loads
from src.errors import *


class NoExRaise(Exception):
    pass


class ExAttrNotMatch(Exception):
    def __init__(self, key, expect, actual):
        self.key = key
        self.expect = expect
        self.actual = actual

    def __repr__(self):
        return "at key: {0}, expect: {1}\nactual: {2}".format(
            self.key, self.expect, self.actual)


def test_right(actual, expect):
    assert actual == expect, 'test fail: expect: {0}, actual: {1}'.format(expect, actual)


def test_error(func, exc, **exc_kvs):
    try:
        func()
    except exc as e:
        for key, value in exc_kvs.items():
            actual_value = getattr(e, key)
            if actual_value != value:
                raise ExAttrNotMatch(key, value, actual_value)
    else:
        raise NoExRaise()


def test_filter_space():
    test_right(loads(' \r\n null  \t\r\n'), None)


def test_parse_null():
    test_right(loads('null'), None)


def test_parse_true():
    test_right(loads('true'), True)


def test_parse_false():
    test_right(loads('false'), False)


def test_parse_number():
    assert loads('123') == 123
    assert loads('123.456') == 123.456
    assert loads('-45.4e-12') == float('-45.4e-12')
    assert loads('12e+3') == float('12e+3')
    assert loads('12E-3') == float('12E-3')
    assert loads('12e6') == float('12e6')
    assert loads('12E130') == float('12E130')


def test_parse_string():
    assert loads("\"\"") == ""
    assert loads("\"abc\"") == "abc"
    assert loads("\"w\\t\\f\"") == "w\t\f"
    assert loads("\"\\\\ \\\" \\/ \\b \\n \\r\"") == "\\ \" / \b \n \r"


def test_parse_array():
    assert loads('[ 12,34    ]') == [12, 34]
    assert loads('[    12,    34   ]') == [12, 34]
    assert loads('[12,34]') == [12, 34]
    assert loads('[ 12, \"WTF?\"]') == [12, "WTF?"]
    assert loads('[ 12, \"WTF?\", true]') == [12, "WTF?", True]
    assert loads('[ 12, \"WTF?\", true, false, null, \"YES!\"]') == [12, "WTF?", True, False, None, "YES!"]
    assert loads('[ 12, \"WTF?\", true, false, null, \"YES!\"]') == [12, "WTF?", True, False, None, "YES!"]
    assert loads('[ "ha?", {"en": 1, "m": 2}]') == ["ha?", {"en": 1, "m": 2}]


def test_parse_obj():
    test_right(loads('{"1": 5}'), {"1": 5})
    test_right(loads('{"my"  : [1,2,3]}'), {"my": [1, 2, 3]})
    test_right(loads('{"my": [2,3,4], "you": [5,6,7]  }'), {"my": [2, 3, 4],
                                                            "you": [5, 6, 7]})
    test_right(loads('{"ha": true}'), {"ha": True})


# error
def test_no_input():
    test_error(lambda: loads(''), NoInput)
    test_error(lambda: loads('\r\t\n'), NoInput)


def test_invalid_input():
    test_error(lambda: loads("ok"), InvalidInput)


def test_root_not_singular():
    test_error(lambda: loads('true n'), RootNotSingular)


def test_invalid_number():
    test_error(lambda: loads('123.'), InvalidInput, at=3)
    test_error(lambda: loads('+123'), InvalidInput, at=-1)


def test_invalid_string():
    test_error(lambda: loads('\"'), MissQuotationMark, at=0)
    test_error(lambda: loads('\" \b \"'), InvalidControlCharacter, at=1)
    test_error(lambda: loads('\" \x1f \"'), InvalidControlCharacter, at=1)


def test_invalid_array():
    test_error(lambda: loads('['), MissBracketForArray, at=0)
    test_error(lambda: loads('[123, ]'), InvalidInput, at=5)
    test_error(lambda: loads('[123, "jjk'), MissQuotationMark)
    test_error(lambda: loads('[null233]'), MissComma)
    test_error(lambda: loads('[truefalse]'), MissComma)


def test_invalid_obj():
    test_error(lambda: loads('{  '), MissBraceForObj)
    test_error(lambda: loads('{ "ssss'), MissQuotationMark)
    test_error(lambda: loads('{ "ss": 1, }'), InvalidInput)
    test_error(lambda: loads('{ "ho": true"false": 1}'), MissComma)


def test_context():
    c = Context('123')
    test_right(c.peek(), '1')
    test_right(c.forward(), '1')
    test_right(c.current(), '1')

    test_right(c.forward(), '2')
    test_right(c.forward(), '3')

    test_right(c.end(), True)

    c = Context('abc')
    assert c.accept('a', 'b', 'c') is True
    assert c.accept('b') is True
    assert c.accept('a') is False

    c = Context('abc')
    assert c.accept('abc') is False


def test():
    test_filter_space()
    test_parse_null()
    test_parse_true()
    test_parse_false()
    test_parse_number()
    test_parse_string()
    test_parse_array()
    test_parse_obj()

    test_no_input()
    test_invalid_input()
    test_root_not_singular()
    test_invalid_number()
    test_invalid_string()
    test_invalid_array()
    test_invalid_obj()

    # test_context()


if __name__ == '__main__':
    test()
    print('all test pass')

