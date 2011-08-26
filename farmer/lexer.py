"""
Farmer's Lexer

This is the lexer to parse a Gherkin input into tokens
"""
import re
from .language import LANGUAGE


class Lexer(object):
    LANGUAGE_PATTERN = re.compile("^\s*#\s*language\s*:\s*([a-zA-Z\-]+)")
    COMMENT = "#"
    FEATURE_ELEMENTS_KEYS = ["feature", "background", "scenario",
                             "scenario_outline", "example"]
    STEP_KEYS = ["given", "when", "then", "and", "but"]
    KEYWORDS = FEATURE_ELEMENTS_KEYS + STEP_KEYS

    def __init__(self):
        self.lang = "en"

    def tokenize(self, source):
        self.source = [(index, line.strip())
                       for index, line in enumerate(source) if line.strip()]
        self.get_meta()
        self.remove_comments()
        try:
            self.keywords = LANGUAGE[self.lang]
            return self.scan(self)
        except KeyError:
            raise KeyError("Language: %s is not defined" % self.lang)

    def get_meta(self):
        for line in self.source:
            language_matcher = Lexer.LANGUAGE_PATTERN.match(line[1])
            if language_matcher:
                self.lang = language_matcher.groups()[0]

    def remove_comments(self):
        self.source = [item for item in self.source
                       if not item[1].startswith("#")]

    def scan(self, source):
        # current line that we are parsing
        self.line = ""
        # collection of all parsed tokens in the form of (:TOKEN_TYPE, value)
        self.tokens = []
        # current feature description.
        self.current_feature_desc = []
        # current multiline. When this is true, all the following lines will be
        # added as a multiline block
        self.should_be_multiline = False
        self.multiline_start = -1
        self.current_multiline = []

        # Read lines of the feature, one by one
        for index, line in self.source:
            self.index = index
            self.line = line.strip()
            if self.line:
                token = self.feature_token()\
                        or self.background_token()\
                        or self.scenario_token()\
                        or self.scenario_outline_token()\
                        or self.examples_token()\
                        or self.tag_token()\
                        or self.step_token()\
                        or self.feature_description_token()\
                        or self.multiline_token()\
                        or self.table_row_token()\

                # unless we get a new token, and the token is proper children
                # of the feature, and current feature description is not empty
                if token and len(self.current_feature_desc) > 0\
                   and token[0] in Lexer.FEATURE_ELEMENTS_KEYS:
                    self.add_feature_description()

                if token and token != Lexer.COMMENT:
                    # either extend the tokens if new token is a list, or
                    # append it
                    if type(token) is list:
                        self.tokens.extend(token)
                    else:
                        self.tokens.append(token)

        # end of file, if there is still non-empty current feature description,
        # insert it into the token list
        if len(self.current_feature_desc) > 0:
            self.add_feature_description()
        return self.tokens

    def add_feature_description(self):
        # set the feature description.
        self.tokens.append(("feature_description",
                           "\n".join(self.current_feature_desc), -1))
        # reset the description to prepare for new feature
        self.current_feature_desc = []

    def add_multiline(self):
        if len(self.current_multiline) > 0\
           and (self.current_multiline[0].startswith("'''")
                or self.current_multiline[0].startswith('"""'))\
           and (self.current_multiline[-1].endswith('"""')
                or self.current_multiline[-1].endswith("'''")):
            # remove the start triplequotes and end triplequotes
            self.current_multiline[0] = self.current_multiline[0][3:]
            self.current_multiline[-1] = self.current_multiline[-1][3:]
            self.tokens.append((
                "Multiline",
                "\n".join([x for x in self.current_multiline if x]),
                "multiline"))
        self.current_multiline = []

    def match_feature_keys(self, keyword, token_type):
        """Match Lexer.FEATURE_KEYS tokens"""
        if not self.should_be_multiline:
            match = re.match("^\s*(%s):\s*(.*)" % keyword, self.line)
            if match:
                groups = match.groups()
                return (token_type, groups[-1], self.index)
        return None

    def feature_token(self):
        return self.match_feature_keys(self.keywords["feature"], "feature")

    def background_token(self):
        return self.match_feature_keys(self.keywords["background"],
                                       "background")

    def scenario_token(self):
        return self.match_feature_keys(self.keywords["scenario"],
                                       "scenario")

    def scenario_outline_token(self):
        return self.match_feature_keys(self.keywords["scenario_outline"],
                                       "scenario_outline")

    def examples_token(self):
        return self.match_feature_keys(self.keywords["examples"], "examples")

    def tag_token(self):
        if not self.should_be_multiline:
            match = re.findall("@(\w+)", self.line)
            return [("tag", tag, self.index) for tag in match]

    def feature_description_token(self):
        # feature description must go after feature
        if not self.should_be_multiline:
            if self.line and len(self.tokens) > 0 and\
            self.tokens[-1][0] == "feature":
                self.current_feature_desc.append(self.line)
        return False

    def table_row_token(self):
        if self.line[0] == "|":
            return ("row", self.line, self.index)

    def step_token(self):
        if not self.should_be_multiline:
            regex_str = "^\s*(%s)\s*(.*)" % (
                "|".join(["(%s)" % self.keywords[key]
                          for key in Lexer.STEP_KEYS]))
            match = re.match(regex_str, self.line)
            if match:
                groups = match.groups()
                return ("step", groups[-1], self.index)
        return None

    def multiline_token(self):
        if len(self.tokens) > 0 and self.tokens[-1][0] == "step":
            if self.line == '"""' and not self.should_be_multiline:
                # start multiline
                self.should_be_multiline = True
                self.multiline_start = self.index
            elif self.line == '"""' and self.should_be_multiline\
               and self.multiline_start < self.index:
                # end multiline
                self.tokens.append(("multiline",
                                    "\n".join(self.current_multiline),
                                    self.multiline_start))
                self.should_be_multiline = False
                self.multiline_start = -1
            elif self.should_be_multiline:
                # process multiline
                if self.index > self.multiline_start:
                    self.current_multiline.append(self.line)
                else:
                    line = self.line[3:].strip()
                    if line:
                        self.current_multiline.append(line)
