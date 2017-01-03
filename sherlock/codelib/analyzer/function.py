from functools import reduce


class Function(object):
    def __init__(self, name, arg_types, return_type, code_generator):
        self.name = name
        self.return_type = return_type
        self.arg_types = arg_types
        self.code_generator = code_generator

    def is_arg_types_match(self, arg_types):
        return reduce(lambda x, y: x & y, [x == arg_types[i] for i, x in enumerate(self.arg_types)])

    def __repr__(self):
        return 'Func(name=%s, arg_types=%s, return_type=%s)' % (self.name, repr(self.arg_types), repr(self.return_type))

class Functions(object):
    def __init__(self):
        self.list = {}

    def __getitem__(self, name):
        return self.list.get(name)

    def append(self, function):
        self.list[function.name] = function

    def __repr__(self):
        return repr(self.list)
