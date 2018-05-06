__all__ = [
    'ParseError',
    'InvalidInput',
    'RootNotSingular',
    'NoInput',
    'MissQuotationMark',
    'InvalidControlCharacter',
    'MissBracketForArray',
    'NoColonAfterKey',
    'MissBraceForObj',
    'MissComma',
    'InvalidUnicodeSurrogate',
]


class ParseError(Exception):
    def __init__(self, at, detail=None):
        self.at = at
        self.detail = detail

    def __repr__(self):
        return 'Error: {type}, at {at}\ndetail: {detail}'.format(
            type=self.__class__, at=self.at, detail=self.detail)


class InvalidInput(ParseError):
    pass


class RootNotSingular(ParseError):
    pass


class NoInput(ParseError):
    pass


class MissQuotationMark(ParseError):
    pass


class InvalidControlCharacter(ParseError):
    pass


class MissBracketForArray(ParseError):
    pass


class NoColonAfterKey(ParseError):
    pass


class MissBraceForObj(ParseError):
    pass


class MissComma(ParseError):
    pass


class InvalidUnicodeSurrogate(ParseError):
    pass
