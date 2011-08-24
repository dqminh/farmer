from .lexer import Lexer
from .node import Feature, Tag

class Parser(object):

    def __init__(self, lexer=None):
        if not lexer:
            lexer = Lexer()
        self.lexer = lexer

    def _find_feature_position(self, lex_struct):
        """Scan for the feature element position in the lex struct list"""
        return [key for key, elem in enumerate(lex_struct)
                       if elem[2] == "feature"]

    def _segment_lex(self, lex_struct):
        """Given a struct list that may contain multiple features, extract
        those features into a feature list. An element of the list will
        resemble a feature, and will contain a list of all feature elements
        such as belonging background, scenarios, etc
        """
        indices = self._find_feature_position(lex_struct)
        feature_list = [lex_struct[i:j]
                    for i, j in zip([0]+indices, indices+[None])]
        # bubble down all tags that do not have any children
        for index, collection in enumerate(feature_list):
            bubble_tags = []
            for element in reversed(collection):
                if element[2] == 'tag':
                    bubble_tags.append(collection.pop())
                else:
                    break
            try:
                for tag in bubble_tags:
                    feature_list[index+1].insert(0, tag)
            except:
                break
        return [item for item in feature_list if len(item) > 0]


    def parse_lex(self, lex_struct):
        feature_list = []
        for struct in lex_struct:
            feature = None
            keyword, name, key_type = struct
            if key_type == "feature":
                feature = Feature(keyword=keyword, name=name,
                                  key_type=key_type)
            if feature:
                feature_list.append(feature)
        return feature_list
