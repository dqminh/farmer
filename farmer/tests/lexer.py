from attest import Tests
from farmer.lexer import Lexer
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

lexer = Tests()

@lexer.test
def parse_feature_keyword():
    lex = Lexer()
    feature = StringIO("Feature: Testing\n")
    tokens = lex.tokenize(feature)
    expected = [("Feature", "Testing", 'feature')]
    assert tokens == expected

@lexer.test
def parse_background_keyword():
    lex = Lexer()
    feature = StringIO("Background: Testing\n")
    tokens = lex.tokenize(feature)
    expected = [("Background", "Testing", 'background')]
    assert tokens == expected

@lexer.test
def parse_scenario_keyword():
    lex = Lexer()
    feature = StringIO("Scenario: Testing\n")
    tokens = lex.tokenize(feature)
    expected = [("Scenario", "Testing", 'scenario')]
    assert tokens == expected

@lexer.test
def parse_scenario_outline_keyword():
    lex = Lexer()
    feature = StringIO("Scenario Outline: Testing\n")
    tokens = lex.tokenize(feature)
    expected = [("Scenario Outline", "Testing", 'scenario_outline')]
    assert tokens == expected

@lexer.test
def parse_examples_keyword():
    lex = Lexer()
    feature = StringIO("Examples: Testing\n")
    tokens = lex.tokenize(feature)
    expected = [("Examples", "Testing", 'examples')]
    assert tokens == expected


@lexer.test
def parse_feature_with_description():
    lex = Lexer()
    feature = StringIO("Feature: Testing\n\tFeature Description")
    tokens = lex.tokenize(feature)
    expected = [("Feature", "Testing", 'feature'),
                ("Feature Description", "Feature Description",
                 "feature_description")]
    assert tokens == expected

@lexer.test
def parse_feature_with_description_and_scenario():
    lex = Lexer()
    feature = StringIO("""
                       Feature: Testing\n
                       \tFeature Description\n
                       Scenario: Hello World
                       """)
    tokens = lex.tokenize(feature)
    expected = [("Feature", "Testing", 'feature'),
                ("Feature Description", "Feature Description",
                 "feature_description"),
                ("Scenario", "Hello World", "scenario")
               ]
    assert tokens == expected

@lexer.test
def parse_feature_with_description_and_background():
    lex = Lexer()
    feature = StringIO("""
                       Feature: Testing\n
                       \tFeature Description\n
                       Background: Hello World
                       """)
    tokens = lex.tokenize(feature)
    expected = [("Feature", "Testing", 'feature'),
                ("Feature Description", "Feature Description",
                 "feature_description"),
                ("Background", "Hello World", "background")
               ]
    assert tokens == expected

@lexer.test
def parse_feature_with_description_and_scenario_outline():
    lex = Lexer()
    feature = StringIO("""
                       Feature: Testing\n
                       \tFeature Description\n
                       Scenario Outline: Hello World
                       """)
    tokens = lex.tokenize(feature)
    expected = [("Feature", "Testing", 'feature'),
                ("Feature Description", "Feature Description",
                 "feature_description"),
                ("Scenario Outline", "Hello World", "scenario_outline")
               ]
    assert tokens == expected

@lexer.test
def parse_step():
    lex = Lexer()
    feature = StringIO("Given I have test")
    tokens = lex.tokenize(feature)
    expected = [("Given", "I have test", 'step')]
    assert tokens == expected

@lexer.test
def parse_feature_with_description_and_scenario_with_step():
    lex = Lexer()
    feature = StringIO("""
                       Feature: Testing\n
                       \tFeature Description\n
                       Scenario: Hello World\n
                       \tGiven I have test\n
                       \tWhen I run it\n
                       \tThen I failed\n
                       """)
    tokens = lex.tokenize(feature)
    expected = [("Feature", "Testing", 'feature'),
                ("Feature Description", "Feature Description",
                 "feature_description"),
                ("Scenario", "Hello World", "scenario"),
                ("Given", "I have test", "step"),
                ("When", "I run it", "step"),
                ("Then", "I failed", "step"),
               ]
    assert tokens == expected

@lexer.test
def parse_feature_with_description_and_multiple_scenarios():
    lex = Lexer()
    feature = StringIO("""
                       Feature: Testing\n
                       \tFeature Description\n
                       Scenario: Hello World\n
                       \tGiven I have test\n
                       \tWhen I run it\n
                       \tThen I failed\n
                       Scenario: Run again\n
                       \tGiven I have 2 tests\n
                       \tWhen I run it\n
                       \tThen I passed\n
                       """)
    tokens = lex.tokenize(feature)
    expected = [("Feature", "Testing", 'feature'),
                ("Feature Description", "Feature Description",
                 "feature_description"),
                ("Scenario", "Hello World", "scenario"),
                ("Given", "I have test", "step"),
                ("When", "I run it", "step"),
                ("Then", "I failed", "step"),
                ("Scenario", "Run again", "scenario"),
                ("Given", "I have 2 tests", "step"),
                ("When", "I run it", "step"),
                ("Then", "I passed", "step"),
               ]
    assert tokens == expected

@lexer.test
def parse_tag_keyword():
    lex = Lexer()
    feature = StringIO("@hello @world")
    tokens = lex.tokenize(feature)
    expected = [("Tag", "hello", "tag"), ("Tag", "world", "tag")]
    assert tokens == expected

@lexer.test
def parse_tag_keyword_with_feature():
    lex = Lexer()
    feature = StringIO("""
                       @test @wip\n
                       Feature: Testing\n
                       """)
    tokens = lex.tokenize(feature)
    expected = [("Tag", "test", "tag"),
                ("Tag", "wip", "tag"),
                ("Feature", "Testing", "feature")
               ]
    assert tokens == expected

@lexer.test
def parse_a_complete_feature():
    lex = Lexer()
    feature = StringIO(
        """
        @wip
        Feature: Befriending\n
        In order to have some friends\n
        As a Facebook user\n
        I want to be able to manage my list of friends\n

        Background:\n
        Given I am the user Ken\n
        And I have friends Barbie, Cloe\n

        @new_friend\n
        Scenario: Adding a new friend\n
        When I add a new friend named Jade\n
        Then I should have friends Barbie, Cloe, Jade\n

        Scenario: Removing a friend\n
        When I remove my friend Cloe\n
        Then I should have friends Barbie\n
        """
        )
    tokens = lex.tokenize(feature)
    expected = [
        ("Tag", "wip", "tag"),
        ("Feature", "Befriending", "feature"),
        ("Feature Description",
         "In order to have some friends\nAs a Facebook user\nI want to be able to manage my list of friends",
         "feature_description"),
        ("Background", "", "background"),
        ("Given", "I am the user Ken", "step"),
        ("And", "I have friends Barbie, Cloe", "step"),
        ("Tag", "new_friend", "tag"),
        ("Scenario", "Adding a new friend", "scenario"),
        ("When", "I add a new friend named Jade", "step"),
        ("Then", "I should have friends Barbie, Cloe, Jade", "step"),
        ("Scenario", "Removing a friend", "scenario"),
        ("When", "I remove my friend Cloe", "step"),
        ("Then", "I should have friends Barbie", "step"),
    ]
    assert tokens == expected
