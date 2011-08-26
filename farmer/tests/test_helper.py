import os

def get_feature(name):
    return os.path.join(os.path.dirname(__file__),
                        "features/%s.feature" % name)
