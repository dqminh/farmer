class Definition(object):
    def __init__(self, keyword=None, name=None, key_type=None):
        self.keyword = keyword
        self.name = name
        self.key_type = key_type

    def __str__(self):
        return "<%s: %s>" % (self.keyword, self.name)


class FeatureDescription(Definition):
    pass


class Tag(Definition):
    pass


class Step(Definition):
    pass


class StepsContainer(object):
    def __init__(self, steps=None):
        self.steps = steps or []

    @property
    def can_has_steps(self):
        return True


class Taggable(object):
    def __init__(self, tags=None):
        self.tags = tags or []

    @property
    def can_has_tags(self):
        return True


class Feature(Definition, Taggable):
    def __init__(self, keyword=None, name=None, key_type=None, tags=None):
        super(Feature, self).__init__(keyword, name, key_type)
        Taggable.__init__(self, tags)
        self.scenario_list = []
        self.background = None

    @classmethod
    def build(cls, element_collection):
        child_steps = []
        feature_elements = []
        # get all elements by associating the steps with its parents and build
        # all elements objects. We will associate the tags later on
        for element_data in reversed(element_collection):
            keyword, name, key_type = element_data
            # get steps
            if key_type == 'step':
                child_steps.append(Step(keyword, name, key_type))
            if key_type in ['scenario', 'scenario_outline', 'background']:
                child_steps = list(reversed(child_steps))
                # get scenario
                if key_type == 'scenario':
                    element = Scenario(keyword, name, key_type, child_steps)
                # get scenario outline
                if key_type == 'scenario_outline':
                    element = ScenarioOutline(keyword, name, key_type, child_steps)
                # get background
                if key_type == 'background':
                    element = Background(keyword, name, key_type, child_steps)
                child_steps = []
                feature_elements.append(element)
            # initialize feature name
            if key_type == 'feature':
                feature_elements.append(Feature(keyword, name, key_type))
            # initialize feature tag
            if key_type == 'tag':
                feature_elements.append(Tag(keyword, name, key_type))
            # initialize description
            if key_type == 'feature_description':
                feature_elements.append(FeatureDescription(keyword, name, key_type))

        # ok, now we associate the tag and description with its correct owner
        index = 1
        while (index < len(feature_elements)):
            try:
                if isinstance(feature_elements[index], Tag):
                    previous = feature_elements[index-1]
                    if previous.can_has_tags:
                        previous.tags.append(feature_elements.pop(index))
                else:
                    index += 1
            except:
                continue
        feature = None
        # get the feature object out
        for index, element in enumerate(feature_elements):
            if isinstance(element, Feature):
                feature = feature_elements.pop(index)
        # concat everything and return the feature object
        for element in feature_elements:
            # add description
            if isinstance(element, FeatureDescription):
                feature.description = element.name
            # add background
            if isinstance(element, Background):
                feature.background = element
            # add scenario outline and scenario
            if isinstance(element, ScenarioOutline)\
               or isinstance(element, Scenario):
                feature.scenario_list.append(element)
        return feature


class Scenario(Definition, Taggable, StepsContainer):
    def __init__(self, keyword, name, key_type, steps=None, tags=None):
        super(Scenario, self).__init__(keyword, name, key_type)
        Taggable.__init__(self, tags)
        StepsContainer.__init__(self, steps)


class ScenarioOutline(Definition, Taggable, StepsContainer):
    def __init__(self, keyword, name, key_type, steps=None, tags=None):
        super(Scenario, self).__init__(keyword, name, key_type)
        Taggable.__init__(self, tags)
        StepsContainer.__init__(self, steps)

class Background(Definition, Taggable, StepsContainer):
    def __init__(self, keyword, name, key_type, steps=None, tags=None):
        super(Scenario, self).__init__(keyword, name, key_type)
        Taggable.__init__(self, tags)
        StepsContainer.__init__(self, steps)
