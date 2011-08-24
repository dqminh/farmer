"""
Farmer's Lexer

This is the lexer to parse a Gherkin input into tokens
"""
import re
from .language import LANGUAGE


class Lexer(object):
    FEATURE_KEYS = ["feature", "background", "scenario", "scenario_outline",
                    "example"]
    STEP_KEYS = ["given", "when", "then", "and", "but"]
    KEYWORDS = FEATURE_KEYS + STEP_KEYS

    def __init__(self, keywords=None):
        if not keywords:
            keywords = LANGUAGE['en']
        self.keywords = keywords

    def tokenize(self, source):
        # current character position that we are parsing
        self.i = 0
        # collection of all parsed tokens in the form of (:TOKEN_TYPE, value)
        self.tokens = []
        # current feature description
        self.current_feature_desc = []
        # current multiline
        self.current_multiline = []
        # Read lines of the feature, one by one
        for line in source:
            self.line = line.strip()
            if self.line:
                token = self.feature_token()\
                        or self.background_token()\
                        or self.scenario_token()\
                        or self.scenario_outline_token()\
                        or self.feature_description_token()\
                        or self.examples_token()\
                        or self.step_token()\
                        or self.tag_token()\
                        or self.table_row_token()\
                        or self.text_token()
                # unless we get a new token, and the token is proper children
                # of the feature, and current feature description is not empty
                if token and len(self.current_feature_desc) > 0\
                   and token[2] in ["scenario", "scenario_outline",
                                    "background"]:
                    # set the feature description. Feature should be the last
                    # token in the token list
                    self.tokens.append(("Feature Description",
                                        "\n".join(self.current_feature_desc),
                                        "feature_description"))
                    # reset the description to prepare for new feature
                    self.current_feature_desc = []
                if token:
                    self.add_multiline()
                    if type(token) is list:
                        self.tokens.extend(token)
                    else:
                        self.tokens.append(token)
        # end of file, if there is still non-empty current feature description,
        # insert it into the token list
        if len(self.current_feature_desc) > 0:
            self.tokens.append(("Feature Description",
                                "\n".join(self.current_feature_desc),
                                "feature_description"))
        # if there are still multiline, insert it into the token list
        self.add_multiline()
        return self.tokens

    def add_multiline(self):
        if len(self.current_multiline) > 0\
           and (self.current_multiline[0].startswith("'''")
                or self.current_multiline[0].startswith('"""'))\
           and (self.current_multiline[-1].endswith('"""')
                or self.current_multiline[-1].endswith("'''")):
            self.tokens.append(("Multiline",
                                "\n".join(self.current_multiline),
                                "multiline"))
        self.current_multiline = []


    def match_token(self, keyword, token_type):
        match = re.match("^\s*(%s):\s*(.*)" % keyword, self.line)
        token = None
        if match:
            groups = match.groups()
            token = (groups[0], groups[-1], token_type)
        return token

    def table_row_token(self):
        if self.line[0] == "|":
            return ("Row", self.line, "row")

    def tag_token(self):
        match = re.findall("@(\w+)", self.line)
        return [("Tag", tag, "tag") for tag in match]

    def step_token(self):
        regex_str = "^\s*(%s)\s*(.*)" % "|".join(["(%s)" % self.keywords[key]
                                                   for key in Lexer.STEP_KEYS])
        match = re.match(regex_str, self.line)
        token = None
        if match:
            groups = match.groups()
            token = (groups[0], groups[-1], "step")
        return token

    def text_token(self):
        # donot accept comment
        if not self.line.startswith("#"):
            self.current_multiline.append(self.line)

    def feature_token(self):
        return self.match_token(self.keywords["feature"], "feature")

    def background_token(self):
        return self.match_token(self.keywords["background"], "background")

    def scenario_token(self):
        return self.match_token(self.keywords["scenario"], "scenario")

    def scenario_outline_token(self):
        return self.match_token(self.keywords["scenario_outline"],
                                "scenario_outline")

    def feature_description_token(self):
        if self.line and len(self.tokens) > 0 and\
           self.tokens[-1][2] == "feature":
            self.current_feature_desc.append(self.line)
        return False

    def examples_token(self):
        return self.match_token(self.keywords["examples"], "examples")
