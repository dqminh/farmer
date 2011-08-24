class Definition(object):
    def __init__(self, keyword, name, key_type):
        self.keyword = keyword
        self.name = name
        self.key_type = key_type


class Tag(Definition):
    pass


class Feature(Definition):
    def __init__(self, keyword, name, key_type):
        super(Feature, self).__init__(keyword, name, key_type)


class Background(Definition):
    pass
