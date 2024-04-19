
class SearchTree(object):

    def __init__(self, value, children = None, parents=None):
        self.value = value
        if children is None:
            self.children = []
        if parents is None:
            self.parents = []

    def __repr__(self):
        return self.value

    def add_child(self, child):
        self.children.append(child)
        child.parents.extend(self.parents)
        child.parents.append(self)