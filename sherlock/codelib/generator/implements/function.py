import ast
from sherlock.errors import SyntaxNotSupportError, FunctionIsNotAnalyzedError
from sherlock.codelib.generator.system_function import is_system_function
from sherlock.codelib.generator.dispatcher import add_generator


@add_generator('Call')
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
        return self.generate_system_function(node, ext_info)
    for x in node.args:
        if isinstance(x, ast.Call):
            new_temp_variable = self.temp_variable.get_new_name()
            self.code_buffer.append(self.dispatch(x))
            self.code_buffer.append('%s=$__return_%s' % (new_temp_variable, x.func.id))
            argument_list.append(new_temp_variable)
        else:
            ext_info['is_arg'] = True
            argument_list.append(self.dispatch(x, ext_info=ext_info))
    arguments_code = ' '.join(argument_list)
    return '%s %s' % (function_name, arguments_code)

@add_generator('FunctionDef')
def generate_functiondef(self, node, ext_info):
    from sherlock.codelib.generator import CodeGenerator, CONTEXT_STATUS_FUNCTION
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

@add_generator('Return')
def generate_return(self, node, ext_info):
    return 'export __return_%s=%s' % (ext_info['func_name'], self.dispatch(node.value))
