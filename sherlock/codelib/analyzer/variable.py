from sherlock.errors import CompileError
from sherlock.codelib.analyzer.factory import ListManagerFactory


class Type(object):
    _VOID = 0
    _NUMBER = 1
    _STRING = 2
    _LIST = 3
    VOID = None
    NUMBER = None
    LIST = None

    def __init__(self, value):
        self.value = value

    @property
    def is_number(self):
        return self.value == Type._NUMBER

    @property
    def is_string(self):
        return self.value == Type._STRING

    @property
    def is_void(self):
        return self.value == Type._VOID

    @property
    def is_list(self):
        return self.value == Type._LIST

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        if self.is_void:
            return 'Void'
        elif self.is_number:
            return 'Number'
        elif self.is_string:
            return 'String'
        elif self.is_list:
            return 'List'
        else:
            return 'Unknown'

Type.NUMBER = Type(Type._NUMBER)
Type.STRING = Type(Type._STRING)
Type.LIST = Type(Type._LIST)
Type.VOID = Type(Type._VOID)

class Variable(object):
    def __init__(self, name, var_type):
        self.name = name
        self.var_type = var_type

    def __repr__(self):
        return 'Var(name=%s, type=%s)' % (self.name, repr(self.var_type))

class Variables(ListManagerFactory):
    pass
