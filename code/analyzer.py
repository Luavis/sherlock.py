import ast
from errors import CompileError, SyntaxNotSupport
from code.generator import CodeGenerator



def str_node(node):
    if isinstance(node, ast.AST):
        fields = [(name, str_node(val)) for name, val in ast.iter_fields(node) if name not in ('left', 'right')]
        rv = '%s(%s' % (node.__class__.__name__, ', '.join('%s=%s' % field for field in fields))
        return rv + ')'
    else:
        return repr(node)

class Type(object):
    _NUMBER = 1
    _STRING = 2
    NUMBER = None
    STRING = None

    def __init__(self, value):
        self.value = value

    @property
    def is_number(self):
        return self.value == Type._NUMBER

    @property
    def is_string(self):
        return self.value == Type._STRING

    def __repr__(self):
        if self.is_number:
            return 'Number'
        elif self.is_string:
            return 'String'
        else:
            return 'Unknown'

Type.NUMBER = Type(Type._NUMBER)
Type.STRING = Type(Type._STRING)


class CodeAnalyzer(object):
    def __init__(self, code, node=None):
        self.code = code
        self.node = node
        if node is None:
            self.node = ast.parse(self.code)

        if not isinstance(self.node, ast.Module):
            raise CompileError()

    def analysis(self):
        for node in self.node.body:
            if isinstance(node, ast.Assign):
                print(self.type_checker(node.value))

    def type_checker(self, node):
        if isinstance(node, ast.BinOp):
            left_type = self.type_checker(node.left)
            right_type = self.type_checker(node.right)

            if isinstance(node.op, ast.Add):
                if left_type.is_number and right_type.is_number:
                    return Type.NUMBER
                else:
                    return Type.STRING
            elif left_type.is_number and right_type.is_number:
                return Type.NUMBER
            else:
                raise CompileError("Can not " + node.op.__class__.__name__ + " operator with string.")
        elif isinstance(node, ast.UnaryOp):
            if isinstance(operand, ast.Num):
                return Type.NUMBER
            else:
                raise SyntaxNotSupport("Not support unary operator except number.")
        elif isinstance(node, ast.Num):
            return Type.NUMBER
        elif isinstance(node, ast.Str):
            return Type.STRING
