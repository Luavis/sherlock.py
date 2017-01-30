from functools import reduce
from sherlock.codelib.analyzer.factory import ListManagerFactory


class Function(object):
    def __init__(self, name, args_type, return_type, code_generator):
        self.name = name
        self.return_type = return_type
        self.args_type = args_type
        self.code_generator = code_generator

    def is_args_type_match(self, args_type):
        return reduce(lambda x, y: x & y, [x == args_type[i] for i, x in enumerate(self.args_type)])

    def __repr__(self):
        return 'Func(name=%s, args_type=%s, return_type=%s)' % (self.name, repr(self.args_type), repr(self.return_type))

class Functions(ListManagerFactory):
    pass
