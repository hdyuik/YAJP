from traceback import print_exc
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
    assert loads(' \r\n null  \t\r\n') is None


def test_parse_null():
    assert loads('null') is None


def test_parse_true():
    assert loads('true') is True


def test_parse_false():
    assert loads('false') is False


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


# error
def test_no_input():
    test_error(lambda: loads(''), NoInput, at=0)
    test_error(lambda: loads('\r\t\n'), NoInput, at=3)


def test_invalid_input():
    test_error(lambda: loads("ok"), InvalidInput, at=0)


def test_root_not_singular():
    test_error(lambda: loads('true n'), RootNotSingular, at=5)


def test_invalid_number():
    test_error(lambda: loads('123.'), InvalidInput, at=4)
    test_error(lambda: loads('+123'), InvalidInput, at=0)


def test_invalid_string():
    test_error(lambda: loads('\"'), MissQuotationMark, at=1)
    test_error(lambda: loads('\" \b \"'), InvalidControlCharacter, at=2)
    test_error(lambda: loads('\" \x1f \"'), InvalidControlCharacter, at=2)


def test_invalid_array():
    test_error(lambda: loads('['), MissBracketForArray, at=1)
    test_error(lambda: loads('[123, ]'), InvalidInput, at=6)
    test_error(lambda: loads('[123, "jjk'), MissQuotationMark)


def test():
    # test_filter_space()
    # test_parse_null()
    # test_parse_true()
    # test_parse_false()
    # test_parse_number()
    # test_parse_string()
    # test_parse_array()

    # test_no_input()
    # test_invalid_input()
    # test_root_not_singular()
    # test_invalid_number()
    # test_invalid_string()
    test_invalid_array()


if __name__ == '__main__':
    test()
    print('test done')

