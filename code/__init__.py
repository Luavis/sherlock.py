import ast
import types
from errors import CompileError, SyntaxNotSupport

CONTEXT_STATUS_GLOBAL = 1
CONTEXT_STATUS_FUNCTION = 2


class CodeGenerator():

    def __init__(self, code=None, node=None, context_status=CONTEXT_STATUS_GLOBAL):
        self.context_status = context_status
        self.code = code
        self.node = node
        self.variable_list = []

    @property
    def is_global(self):
        return self.context_status == CONTEXT_STATUS_GLOBAL        

    def generate_assign(self, node):
        target_code = ''
        if isinstance(node.targets[0], ast.Name):
            target_code = self._generate(node.targets[0])
        else:
            raise CompileError()

        value_code = self._generate(node.value)
        if value_code is None:
            raise CompileError()
        return target_code + '=' + value_code

    def generate_name(self, node):
        if isinstance(node.ctx, ast.Store) or isinstance(node.ctx, ast.Param):
            return 'export ' + node.id if self.is_global else 'local ' + node.id
        else:
            return '$' + node.id

    def generate(self):
        if self.node is None:
            self.node = ast.parse(self.code)
        if isinstance(self.node, ast.Module):
            return '\n'.join([self._generate(x) for x in self.node.body])
        elif isinstance(self.node, ast.FunctionDef):
            if not len(self.node.decorator_list) == 0:
                raise SyntaxNotSupport('Function decoration is not support yet.')
            arguments_code = '\n'.join([self._generate(x) + '=$' + str(i + 1) for i, x in enumerate(self.node.args.args)])
            body_code = '\n'.join([self._generate(x) for x in self.node.body])
            return 'function %s() {\n%s\n%s\n}' % (self.node.name, arguments_code, body_code)
        else:
            raise CompileError()

    def generate_expr(self, node):
        return self._generate(node.value)

    def generate_call(self, node):
        if not node.kwargs is None:
            raise SyntaxNotSupport('Keyword arguments is not support yet')
        funciton_name = node.func.id
        arguments_code = ' '.join([self._generate(x) for x in node.args])
        return '%s %s' % (funciton_name, arguments_code)

    def generate_binop(self, node):
        if isinstance(node.op, ast.Add):
            return self._generate(node.left) + '+' + self._generate(node.right)
        else:
            raise SyntaxNotSupport(node.op.__class__.__name__ + " operation is not support yet.")

    def _generate(self, node):
        # print('  ' + str_node(node))
        if isinstance(node, ast.Assign):
            return self.generate_assign(node)
        elif isinstance(node, ast.Name):
            return self.generate_name(node)
        elif isinstance(node, ast.Expr):
            return self.generate_expr(node)
        elif isinstance(node, ast.Call):
            return self.generate_call(node)
        elif isinstance(node, ast.Num):
            return str(node.n)
        elif isinstance(node, ast.BinOp):
            return self.generate_binop(node)
        elif isinstance(node, ast.Str):
            return '"' + node.s.replace('"','\\"') + '"'
        elif isinstance(node, ast.FunctionDef):
            generator = CodeGenerator(node=node, context_status=CONTEXT_STATUS_FUNCTION)
            return generator.generate()
        else:
            return ''
