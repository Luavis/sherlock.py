class ListManagerFactory(object):
    def __init__(self):
        self.list = {}

    def __getitem__(self, name):
        return self.list.get(name)

    def append(self, elem):
        self.list[elem.name] = elem

    def __repr__(self):
        return repr(self.list)
