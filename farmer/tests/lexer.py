from attest import Tests
from farmer.lexer import Lexer
from .test_helper import get_feature
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

lexer = Tests()

@lexer.test
def get_language():
    lex = Lexer()
    with open(get_feature("language")) as handler:
        lex.tokenize(handler)
        assert lex.lang == "en"
        assert len(lex.source) == 1

@lexer.test
def parse_feature_keyword():
    lex = Lexer()
    feature = StringIO("Feature: Testing\n")
    tokens = lex.tokenize(feature)
    expected = [("feature", "Testing", 0)]
    assert tokens == expected

@lexer.test
def parse_background_keyword():
    lex = Lexer()
    feature = StringIO("Background: Testing\n")
    tokens = lex.tokenize(feature)
    expected = [("background", "Testing", 0)]
    assert tokens == expected

@lexer.test
def parse_scenario_keyword():
    lex = Lexer()
    feature = StringIO("Scenario: Testing\n")
    tokens = lex.tokenize(feature)
    expected = [("scenario", "Testing", 0)]
    assert tokens == expected

@lexer.test
def parse_scenario_outline_keyword():
    lex = Lexer()
    feature = StringIO("Scenario Outline: Testing\n")
    tokens = lex.tokenize(feature)
    expected = [("scenario_outline", "Testing", 0)]
    assert tokens == expected

@lexer.test
def parse_examples_keyword():
    lex = Lexer()
    feature = StringIO("Examples: Testing\n")
    tokens = lex.tokenize(feature)
    expected = [("examples", "Testing", 0)]
    assert tokens == expected

@lexer.test
def parse_tag_keyword():
    lex = Lexer()
    feature = StringIO("@hello @world")
    tokens = lex.tokenize(feature)
    expected = [("tag", "hello", 0), ("tag", "world", 0)]
    assert tokens == expected

@lexer.test
def parse_step():
    lex = Lexer()
    feature = StringIO("Given I have test")
    tokens = lex.tokenize(feature)
    expected = [("step", "I have test", 0)]
    assert tokens == expected

@lexer.test
def simple_feature():
    lex = Lexer()
    with open(get_feature("simple")) as handle:
        tokens = lex.tokenize(handle)
        expected = [("feature", "Feature Text", 0),
                    ("scenario", "Reading a Scenario", 1),
                    ("step", "there is a step", 2)]
        assert tokens == expected

@lexer.test
def simple_feature_with_multiline():
    lex = Lexer()
    with open(get_feature("simple_with_multiline")) as handle:
        tokens = lex.tokenize(handle)
        expected = [("feature", "Feature Text", 0),
                    ("scenario", "Reading a Scenario", 1),
                    ("step", "there is a step", 2),
                    ("multiline",
                     "This is a multiline\nGiven that we have it"
                     , 3)]
        assert tokens == expected

@lexer.test
def feature_with_description_and_scenario():
    lex = Lexer()
    with open(get_feature("simple_with_feature_description")) as feature:
        tokens = lex.tokenize(feature)
        expected = [("feature", "Feature Text", 0),
                    ("feature_description",
                     "We should be able to read a feature",
                     -1),
                    ("scenario", "Reading a Scenario", 2),
                    ("step", "there is a step", 3)]
        assert tokens == expected

@lexer.test
def feature_with_comment():
    lex = Lexer()
    with open(get_feature("simple_with_comments")) as handle:
        tokens = lex.tokenize(handle)
        expected = [("feature", "Feature Text", 1),
                    ("scenario", "Reading a Scenario", 3),
                    ("step", "there is a step", 5)]
        assert tokens == expected

@lexer.test
def parse_table_layout():
    lex = Lexer()
    feature = StringIO("|func|name|\n|hello|world|")
    tokens = lex.tokenize(feature)
    expected = [("row", "|func|name|", 0), ("row", "|hello|world|", 1)]
    assert tokens == expected

@lexer.test
def complex_feature():
    lex = Lexer()
    with open(get_feature("complex")) as feature:
        tokens = lex.tokenize(feature)
        expected = [
            ("tag", "tag1", 2),
            ("tag", "tag2", 2),
            ("feature", "Feature Text", 3),
            ("feature_description",
             "In order to test multiline forms\nAs a ragel writer\nI need to check for complex combinations",
            -1),

            ("background", "", 12),
            ("step", "this is a background step", 13),
            ("step", "this is another one", 14),

            ("tag", "tag3", 16),
            ("tag", "tag4", 16),
            ("scenario", "Reading a Scenario", 17),
            ("step", "there is a step", 18),
            ("step", "not another step", 19),

            ("tag", "tag3", 21),
            ("scenario", "Reading a second scenario", 22),
            ("step", "a third step with a table", 24),
            ("row", "|a|b|", 25),
            ("row", "|c|d|", 26),
            ("row", "|e|f|", 27),
            ("step", "I am still testing things", 28),
            ("row", "|g|h|", 29),
            ("row", "|e|r|", 30),
            ("row", "|k|i|", 31),
            ("row", "|n||", 32),
            ("step", "I am done testing these tables", 33),
            ("step", "I am happy", 35),

            ("scenario", "Hammerzeit", 37),
            ("step", "All work and no play", 38),
            ("multiline",
             "Makes Homer something something\nAnd something else",
             39),
            ("step", "crazy", 43)
        ]
        for index , item in enumerate(tokens):
            assert tokens[index] == expected[index]
