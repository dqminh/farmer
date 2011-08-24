from attest import Tests
from farmer.lexer import Lexer
from farmer.parser import Parser
from farmer.node import Feature

parser = Tests()

@parser.test
def parse_simple_only_feature():
    parse = Parser(Lexer())
    feature_list = parse.parse_lex([("Feature", "Testing", "feature")])
    assert isinstance(feature_list, list)
    assert isinstance(feature_list[0], Feature)
    inst = feature_list[0]
    assert inst.keyword == "Feature"
    assert inst.name == "Testing"
    assert inst.key_type == "feature"

@parser.test
def parse_without_feature():
    parse = Parser(Lexer())
    feature_list = parse.parse_lex([("Given", "Testing", "step")])
    assert len(feature_list) == 0

@parser.test
def scan_feature_position():
    parse = Parser()
    feature_pos = parse._find_feature_position([
        ("Feature", "Testing", 'feature'),
        ("Feature Description", "Feature Description", "feature_description"),
        ("Scenario", "Hello World", "scenario"),
        ("Given", "I have test", "step"),
        ("When", "I run it", "step"),
        ("Then", "I failed", "step"),

        ("Feature", "Testing", 'feature'),
        ("Feature Description", "Feature Description", "feature_description"),
        ("Scenario", "Hello World", "scenario"),
        ("Given", "I have test", "step"),
        ("When", "I run it", "step"),
        ("Then", "I failed", "step"),
    ])
    expected = [0, 6]
    assert feature_pos == expected

@parser.test
def segment_lex():
    parse = Parser()
    segment_feature = parse._segment_lex([
        ("Tag", "wip", 'tag'),
        ("Feature", "Testing", 'feature'),
        ("Feature Description", "Feature Description", "feature_description"),
        ("Scenario", "Hello World", "scenario"),
        ("Given", "I have test", "step"),
        ("When", "I run it", "step"),
        ("Then", "I failed", "step"),

        ("Tag", "wip", 'tag'),
        ("Feature", "Testing", 'feature'),
        ("Feature Description", "Feature Description", "feature_description"),
        ("Tag", "javascript", 'tag'),
        ("Scenario", "Hello World", "scenario"),
        ("Given", "I have test", "step"),
        ("When", "I run it", "step"),
        ("Then", "I failed", "step"),
    ])
    expected = [
        [
            ("Tag", "wip", 'tag'),
            ("Feature", "Testing", 'feature'),
            ("Feature Description", "Feature Description", "feature_description"),
            ("Scenario", "Hello World", "scenario"),
            ("Given", "I have test", "step"),
            ("When", "I run it", "step"),
            ("Then", "I failed", "step"),
        ],
        [
            ("Tag", "wip", 'tag'),
            ("Feature", "Testing", 'feature'),
            ("Feature Description", "Feature Description", "feature_description"),
            ("Tag", "javascript", 'tag'),
            ("Scenario", "Hello World", "scenario"),
            ("Given", "I have test", "step"),
            ("When", "I run it", "step"),
            ("Then", "I failed", "step"),
        ]
    ]
    assert segment_feature == expected

@parser.test
def parse_and_associate_tag():
    pass
