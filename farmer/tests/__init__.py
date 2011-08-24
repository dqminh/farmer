from attest import Tests
from .lexer import lexer
from .parser import parser

collection = Tests([
    lexer, parser
])
