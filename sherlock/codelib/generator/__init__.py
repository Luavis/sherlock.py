import ast
import types
from sherlock.codelib.generator.dispatcher import CONTEXT_STATUS_GLOBAL, CONTEXT_STATUS_FUNCTION
from sherlock.errors import CompileError, SyntaxNotSupportError, FunctionIsNotAnalyzedError
from sherlock.codelib.analyzer.variable import Variables, Type
from sherlock.codelib.analyzer.function import Functions
from sherlock.codelib.generator.temp_variable import TempVariableManager
from sherlock.codelib.generator.binop import generate_binop, generate_numeric_op
from sherlock.codelib.generator.system_function import is_system_function, generate_system_function
from sherlock.codelib.generator.dispatcher import generator_dipatcher


class CodeGenerator(object):

    def __init__(
        self,
        code=None,
        node=None,
        context_status=CONTEXT_STATUS_GLOBAL,
        functions=Functions(),
        variables=Variables(),
        function_info=None
    ):
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

    def generate(self):
        if self.node is None:
            self.node = ast.parse(self.code)
        if isinstance(self.node, ast.Module):
            for x in self.node.body:
                self.code_buffer.append(self._generate(x))
            return '\n'.join(self.code_buffer) + '\n'
        elif isinstance(self.node, ast.FunctionDef):
            if self.function_info is None:
                raise FunctionIsNotAnalyzedError(self.node.name)
            if not len(self.node.decorator_list) == 0:
                raise SyntaxNotSupportError('Function decoration is not support yet.')
            arguments_list = []
            for i, x in enumerate(self.node.args.args):
                if self.function_info.args_type[i].is_list:
                    arguments_list.append('declare -a %s=("${!%i}")' % (self._generate(x), i + 1))
                else:
                    arguments_list.append('%s=$%i' % (self._generate(x), i + 1))
            arguments_code = '\n'.join(arguments_list)
            for x in self.node.body:
                self.code_buffer.append(self._generate(x, {'func_name': self.node.name}))
            return 'function %s() {\n%s\n%s\n}' % (self.node.name, arguments_code, '\n'.join(self.code_buffer))
        else:
            raise CompileError("code section must be function or module node")

    def _generate(self, node, ext_info={}):
        return generator_dipatcher(self, node, ext_info)

    def generate_num(self, node, ext_info):
        return str(node.n)

    def generate_assign(self, node, ext_info):
        target_code = ''
        if isinstance(node.targets[0], ast.Name):
            target_code = self._generate(node.targets[0])
        else:
            raise CompileError()

        if isinstance(node.value, ast.Call):
            return '%s\n%s=$__return_%s' % (
                self._generate(node.value),
                target_code,
                node.value.func.id
            )
        else:
            ext_info = {}
            value_code = self._generate(node.value, ext_info)
            extra_code = ext_info.get('extra_code', '')
            if value_code is None:
                raise CompileError()

            return extra_code + target_code + '=' + value_code

    def generate_aug_assign(self, node, ext_info):
        tmp_name = self.temp_variable.get_new_name()
        tmp_assign_code = '%s=%s' % (
            tmp_name,
            self._generate(node.value)
        )
        self.code_buffer.append(tmp_assign_code)
        target = self._generate(node.target)
        target_type = self.get_type(node.target)
        if target_type.is_number:
            op = generate_numeric_op(self, node.op, ext_info)
            return '%s=$(( $%s %s $%s ))'% (
                target,
                target,
                op,
                tmp_name
            )
        elif target_type.is_string:
            if isinstance(node.op, ast.Add):
                return '%s=%s$%s'% (
                    target,
                    target,
                    tmp_name
                )
            else:
                raise SyntaxNotSupportError(
                    "%s operation is not support yet."
                    % node.op.__class__.__name__
                )

    def generate_return(self, node, ext_info):
        return 'export __return_%s=%s' % (ext_info['func_name'], self._generate(node.value))

    def generate_pass(self, node, ext_info):
        return ''

    def generate_print(self, node, ext_info):
        return 'echo %s' % ' '.join([self._generate(value) for value in node.values])

    def generate_arg(self, node, ext_info):
        return 'local ' + node.arg

    def generate_str(self, node, ext_info):
        return '"' + node.s.replace('"','\\"') + '"'

    def generate_binop(self, node, ext_info):
        if ext_info.get('extra_code') is None:
            ext_info['extra_code'] = ''

        ret, ext_info['extra_code'] = generate_binop(self, node, ext_info)
        return ret

    def generate_name(self, node, ext_info={'is_arg': False}):
        is_arg = ext_info.get('is_arg', False)
        if isinstance(node.ctx, ast.Store) or isinstance(node.ctx, ast.Param):
            return 'export ' + node.id if self.is_global else 'local ' + node.id
        else:
            if is_arg and self.get_type(node).is_list:
                return node.id + '[@]'
            else:
                return '$' + node.id

    def generate_expr(self, node, ext_info):
        if isinstance(node.value, ast.Str):
            # remove line comment
            return ''
        else:
            return self._generate(node.value)

    def generate_call(self, node, ext_info={}):
        if hasattr(node, 'kwargs'):
            if not node.kwargs is None:
                raise SyntaxNotSupportError('Keyword arguments is not support yet.')
        elif not len(node.keywords) == 0:
            raise SyntaxNotSupportError('Keyword arguments is not support yet.')
        function_name = node.func.id
        if len(node.args) is 0:
            return '%s' % function_name
        argument_list = []
        if is_system_function(function_name):
            return generate_system_function(self, node, ext_info)
        for x in node.args:
            if isinstance(x, ast.Call):
                new_temp_variable = self.temp_variable.get_new_name()
                self.code_buffer.append(self._generate(x))
                self.code_buffer.append('%s=$__return_%s' % (new_temp_variable, x.func.id))
                argument_list.append(new_temp_variable)
            else:
                ext_info['is_arg'] = True
                argument_list.append(self._generate(x, ext_info=ext_info))
        arguments_code = ' '.join(argument_list)
        return '%s %s' % (function_name, arguments_code)

    def generate_functiondef(self, node, ext_info):
        function_info = self.functions[node.name]
        if function_info is None:
            raise FunctionIsNotAnalyzedError(node.name)
        else:
            generator = CodeGenerator(
                node=node,
                context_status=CONTEXT_STATUS_FUNCTION,
                function_info=function_info,
            )
            return generator.generate()

    def generate_list(self, node, ext_info):
        for x in node.elts:
            if isinstance(x, ast.List):
                raise SyntaxNotSupportError(
                    "Multiple dimension array is not support in shellscript language."
                )
        return '(%s)' % ' '.join([self._generate(x, ext_info) for x in node.elts])

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
