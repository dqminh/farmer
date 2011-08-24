from attest import Tests
from farmer.lexer import Lexer
from farmer.parser import Parser
from farmer.node import Feature, Tag

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
def parse_and_associate_tag_with_feature():
    parse = Parser()
    feature_list = parse.parse_lex([
        ("Tag", "wip", 'tag'),
        ("Feature", "Testing", 'feature'),
        ("Feature Description", "Feature Description", "feature_description"),
        ("Scenario", "Hello World", "scenario"),
        ("Given", "I have test", "step"),
        ("When", "I run it", "step"),
        ("Then", "I failed", "step"),
    ])
    feature = feature_list[0]
    # assert feature
    assert isinstance(feature, Feature)
    assert feature.name == "Testing"
    assert len(feature.tags) == 1
    assert isinstance(feature.tags[0], Tag)
    assert feature.description == "Feature Description"
    # assert scenarios
    assert len(feature.scenario_list) == 1
    assert feature.scenario_list[0].name == "Hello World"
    # assert steps
    assert len(feature.scenario_list[0].steps) == 3
    assert feature.scenario_list[0].steps[0].keyword == "Given"
    assert feature.scenario_list[0].steps[0].name == "I have test"
    assert feature.scenario_list[0].steps[1].keyword == "When"
    assert feature.scenario_list[0].steps[1].name == "I run it"
    assert feature.scenario_list[0].steps[2].keyword == "Then"
    assert feature.scenario_list[0].steps[2].name == "I failed"

@parser.test
def now_we_have_tag_with_non_feature():
    parse = Parser()
    feature_list = parse.parse_lex([
        ("Tag", "wip", 'tag'),
        ("Feature", "Testing", 'feature'),
        ("Feature Description", "Feature Description", "feature_description"),
        ("Tag", "javascript", 'tag'),
        ("Scenario", "Hello World", "scenario"),
        ("Given", "I have test", "step"),
        ("When", "I run it", "step"),
        ("Then", "I failed", "step"),
    ])
    feature = feature_list[0]
    # assert feature
    assert len(feature.scenario_list[0].tags) == 1
    assert feature.scenario_list[0].tags[0].name == "javascript"

@parser.test
def we_can_even_have_multiple_tags():
    parse = Parser()
    feature_list = parse.parse_lex([
        ("Tag", "wip", 'tag'),
        ("Tag", "test", 'tag'),
        ("Feature", "Testing", 'feature'),
        ("Feature Description", "Feature Description", "feature_description"),
        ("Tag", "javascript", 'tag'),
        ("Tag", "later", 'tag'),
        ("Scenario", "Hello World", "scenario"),
        ("Given", "I have test", "step"),
        ("When", "I run it", "step"),
        ("Then", "I failed", "step"),
    ])
    feature = feature_list[0]
    # assert feature
    assert set([x.name for x in feature.tags]) <= set(["wip", "test"])
    assert set([x.name for x in feature.scenario_list[0].tags])\
            <= set(["javascript", "later"])

@parser.test
def multiple_feature_is_ok():
    parse = Parser()
    feature_list = parse.parse_lex([
        ("Tag", "wip", 'tag'),
        ("Tag", "test", 'tag'),
        ("Feature", "Testing", 'feature'),
        ("Feature Description", "Feature Description", "feature_description"),
        ("Tag", "javascript", 'tag'),
        ("Tag", "later", 'tag'),
        ("Scenario", "Hello World", "scenario"),
        ("Given", "I have test", "step"),
        ("When", "I run it", "step"),
        ("Then", "I failed", "step"),

        ("Tag", "wip", 'tag'),
        ("Tag", "test", 'tag'),
        ("Feature", "Testing", 'feature'),
        ("Feature Description", "Feature Description", "feature_description"),
        ("Tag", "javascript", 'tag'),
        ("Tag", "later", 'tag'),
        ("Scenario", "Hello World", "scenario"),
        ("Given", "I have test", "step"),
        ("When", "I run it", "step"),
        ("Then", "I failed", "step"),
    ])
    assert len(feature_list) == 2
    # assert feature
    assert set([x.name for x in feature_list[0].tags]) <= set(["wip", "test"])
    assert set([x.name for x in feature_list[1].scenario_list[0].tags])\
            <= set(["javascript", "later"])
