import ast
from errors import CompileError, SyntaxNotSupport
from codelib.generator import CodeGenerator


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

class Variable(object):
    def __init__(self, name, var_type):
        self.name = name
        self.var_type = var_type

class CodeAnalyzer(object):
    def __init__(self, code, module_node=None):
        self.code = code
        self.module_node = module_node
        if module_node is None:
            self.module_node = ast.parse(self.code)

        if not isinstance(self.module_node, ast.Module):
            raise CompileError()

    def analysis(self):
        for node in self.module_node.body:
            variable_list = []
            if isinstance(node, ast.Assign):
                variable_list = self.get_type(node.value)

    def analysis_function(self, function_node, arg_types=[]):
        for node in function_node.body:
            if isinstance(node, ast.Assign):
                self.get_type(node.value)

    def get_function_return_type(self, function_name, arg_types=[]):
        for node in self.module_node.body:
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                self.analysis_function(node, arg_types)

    def get_type(self, node):
        if isinstance(node, ast.BinOp):
            left_type = self.get_type(node.left)
            right_type = self.get_type(node.right)

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
        elif isinstance(node, ast.Call):
            arg_types = [self.get_type(arg) for arg in node.args]
            return self.get_function_return_type(node.func.id, arg_types)
