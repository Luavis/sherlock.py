import ast
from errors import CompileError, SyntaxNotSupportError, TypeMismatchError
from codelib.generator import CodeGenerator
from codelib.analyzer.variable import Type, Variable, Variables
from codelib.analyzer.function import Function, Functions


def str_node(node):
    if isinstance(node, ast.AST):
        fields = [(name, str_node(val)) for name, val in ast.iter_fields(node) if name not in ('left', 'right')]
        rv = '%s(%s' % (node.__class__.__name__, ', '.join('%s=%s' % field for field in fields))
        return rv + ')'
    else:
        return repr(node)

class CodeAnalyzer(object):
    def __init__(self, code):
        self.code = code
        self.module_node = ast.parse(self.code)
        self.functions = Functions()
        if not isinstance(self.module_node, ast.Module):
            raise CompileError()

    def analysis(self):
        variables = Variables()
        for node in self.module_node.body:
            if isinstance(node, ast.Assign):
                self.analysis_assign_node(variables, node)
        generator = CodeGenerator(self.code, functions= self.functions,variables=variables)
        return generator

    def analysis_function(self, function_node, arg_types=[]):
        variables = Variables()
        return_type = Type.VOID

        for node in function_node.body:
            if isinstance(node, ast.Assign):
                self.analysis_assign_node(variables, node)
            elif isinstance(node, ast.Return):
                return_type = self.get_type(node.value)
                if return_type is None:
                    return_type = Type.VOID
        generator = CodeGenerator(self.code,variables=variables)
        return generator, return_type

    def analysis_assign_node(self, variables, node):
        if len(node.targets) > 1:
            raise SyntaxNotSupportError('Tuple assignment is not support yet.')
        target = node.targets[0]
        variables.append(Variable(name=target.id, var_type=self.get_type(node.value)))

    def get_function_return_type(self, function_name, arg_types=[]):
        function = self.functions[function_name]
        if function is not None:
            if function.is_arg_types_match(arg_types):
                return function.return_type
            else:
                raise TypeMismatchError("Function '%s' parameter type is not match", function_name)
        else:
            for node in self.module_node.body:
                if isinstance(node, ast.FunctionDef) and node.name == function_name:
                    generator, return_type = self.analysis_function(node, arg_types)
                self.functions.append(Function(function_name, arg_types, return_type, generator))

            return return_type

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
                raise CompileError("Can not '%s' operator with string." % node.op.__class__.__name__)
        elif isinstance(node, ast.UnaryOp):
            if isinstance(operand, ast.Num):
                return Type.NUMBER
            else:
                raise SyntaxNotSupportError("Not support unary operator except number.")

        elif isinstance(node, ast.Num):
            return Type.NUMBER

        elif isinstance(node, ast.Str):
            return Type.STRING
        elif isinstance(node, ast.Call):
            arg_types = [self.get_type(arg) for arg in node.args]
            return self.get_function_return_type(node.func.id, arg_types)
