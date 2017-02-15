import ast
import types
from sherlock.errors import CompileError, SyntaxNotSupportError, FunctionIsNotAnalyzedError
from sherlock.codelib.analyzer.variable import Variables, Type
from sherlock.codelib.analyzer.function import Functions
from sherlock.codelib.generator.temp_variable import TempVariableManager

CONTEXT_STATUS_GLOBAL = 1
CONTEXT_STATUS_FUNCTION = 2


class CodeGenerator(object):

    EXTENSIONS = [
        'sherlock.codelib.generator.implements.simple_generator',
        'sherlock.codelib.generator.implements.compare_op',
        'sherlock.codelib.generator.implements.statement',
        'sherlock.codelib.generator.implements.binop',
        'sherlock.codelib.generator.implements.assignment',
        'sherlock.codelib.generator.implements.function',
        'sherlock.codelib.generator.implements.importing',
        'sherlock.codelib.system_function',
        'sherlock.codelib.cmd',
    ]

    def __init__(
        self,
        code=None,
        node=None,
        context_status=CONTEXT_STATUS_GLOBAL,
        functions=Functions(),
        variables=Variables(),
        function_info=None
    ):
        for extension in CodeGenerator.EXTENSIONS:
            __import__(extension)

        self.context_status = context_status
        self.global_generator = None
        self.functions = functions
        self.code = code
        self.node = node
        self.variables = variables
        self.temp_variable = TempVariableManager('__temp_var')
        self.code_buffer = []
        self.function_info = function_info

    @property
    def is_global(self):
        return self.context_status == CONTEXT_STATUS_GLOBAL

    def append_code(self, code):
        self.code_buffer.append(code)

    def dispatch(self, node, ext_info={}):
        from sherlock.codelib.generator.dispatcher import AST_NODE_DISPATCHER
        generator = AST_NODE_DISPATCHER.get(node.__class__)
        if generator is None:
            raise SyntaxNotSupportError("%s is not support yet." % node.__class__.__name__)
        return generator(self, node, ext_info)

    def generate(self):
        if self.node is None:
            self.node = ast.parse(self.code)
        if isinstance(self.node, ast.Module):
            for x in self.node.body:
                code_slice = self.dispatch(x)
                if code_slice is not None:
                    self.code_buffer.append(code_slice)
            return '\n'.join(self.code_buffer) + '\n'
        elif isinstance(self.node, ast.FunctionDef):
            if self.function_info is None:
                raise FunctionIsNotAnalyzedError(self.node.name)
            if not len(self.node.decorator_list) == 0:
                raise SyntaxNotSupportError('Function decoration is not support yet.')
            arguments_list = []
            for i, x in enumerate(self.node.args.args):
                if self.function_info.args_type[i].is_list:
                    arguments_list.append('declare -a %s=("${!%i}")' % (self.dispatch(x), i + 1))
                else:
                    arguments_list.append('%s=$%i' % (self.dispatch(x), i + 1))
            arguments_code = '\n'.join(arguments_list)
            for x in self.node.body:
                self.code_buffer.append(self.dispatch(x, {'func_name': self.node.name}))
            return 'function %s() {\n%s\n%s\n}' % (self.node.name, arguments_code, '\n'.join(self.code_buffer))
        else:
            raise CompileError("code section must be function or module node")

    def get_type(self, node):
        if isinstance(node, ast.Num):
            return Type.NUMBER
        elif isinstance(node, ast.Str):
            return Type.STRING
        elif isinstance(node, ast.Name):
            if self.variables[node.id] is not None:
                return self.variables[node.id].var_type
            else:
                return Type.VOID
        elif isinstance(node, ast.BinOp):
            if self.get_type(node.left).is_number and self.get_type(node.right).is_number:
                return Type.NUMBER
            elif self.get_type(node.left).is_string or self.get_type(node.right).is_string:
                return Type.STRING
        elif isinstance(node, ast.Call):
            return self.functions[node.func.id].return_type
        else:
            return Type.VOID
