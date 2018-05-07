from yajp import *


class NoExRaise(Exception):
    pass


class ExNotMatch(Exception):
    pass


def test_right(actual, expect):
    assert actual == expect, 'test fail: expect: {0}, actual: {1}'.format(expect, actual)


def test_error(func):
    try:
        func()
    except DecodeError as e:
        pass
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
    test_right(loads('\"\\u20AC\\u5b87\"'), "€宇")
    test_right(loads('\"\\uD834\\uDD1E\"'), '𝄞')


def test_parse_array():
    test_right(loads('[ 12,34    ]'), [12, 34])
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
    test_error(lambda: loads(''))
    test_error(lambda: loads('\r\t\n'))


def test_root_not_singular():
    test_error(lambda: loads('true, null'))


def test_invalid_number():
    test_error(lambda: loads('123.'))
    test_error(lambda: loads('+123'))


def test_invalid_string():
    test_error(lambda: loads('\"'))
    test_error(lambda: loads('\" \b \"'))
    test_error(lambda: loads('\" \x1f \"'))
    test_error(lambda: loads('\"\\u0ac   \"'))
    test_error(lambda: loads('\"\\uZ980 \"'))
    test_error(lambda: loads('\"\\u0000'))
    test_error(lambda: loads('\"\\uD834WTF?\"'))
    test_error(lambda: loads('\"\\uD834\\uC890 \"'))

    # test_right(loads('\"\\uD834\\uDD1E\"'), '𝄞')


def test_invalid_array():
    test_error(lambda: loads('['))
    test_error(lambda: loads('[123, ]'))
    test_error(lambda: loads('[123, "jjk'))
    test_error(lambda: loads('[null233]'))
    test_error(lambda: loads('[truefalse]'))


def test_invalid_obj():
    test_error(lambda: loads('{  '))
    test_error(lambda: loads('{ "ssss'))
    test_error(lambda: loads('{ "ss": 1, }'))
    test_error(lambda: loads('{ "ho": true"false": 1}'))


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
    test_root_not_singular()
    test_invalid_number()
    test_invalid_string()
    test_invalid_array()
    test_invalid_obj()


if __name__ == '__main__':
    test()
    print('all test pass')
