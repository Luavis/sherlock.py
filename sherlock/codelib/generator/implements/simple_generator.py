import ast
from sherlock.errors import CompileError, SyntaxNotSupportError
from sherlock.codelib.generator.dispatcher import add_generator


@add_generator('Num')
def generate_num(self, node, ext_info):
    return str(node.n)

@add_generator()
def generate_numeric_op(self, node, ext_info):
    if isinstance(node, ast.Add):
        return '+'
    elif isinstance(node, ast.Sub):
        return '-'
    elif isinstance(node, ast.Mult):
        return '*'
    elif isinstance(node, ast.Div):
        return '/'
    else:
        return ''

@add_generator('Pass')
def generate_pass(self, node, ext_info):
    return ''

@add_generator('Print')
def generate_print(self, node, ext_info):
    return 'echo %s' % ' '.join([self.dispatch(value) for value in node.values])

@add_generator('arg')
def generate_arg(self, node, ext_info):
    return 'local ' + node.arg

@add_generator('Str')
def generate_str(self, node, ext_info):
    return '"' + node.s.replace('"','\\"') + '"'

@add_generator('Name')
def generate_name(self, node, ext_info={'is_arg': False}):
    is_arg = ext_info.get('is_arg', False)
    if isinstance(node.ctx, ast.Store) or isinstance(node.ctx, ast.Param):
        return 'export ' + node.id if self.is_global else 'local ' + node.id
    else:
        if is_arg and self.get_type(node).is_list:
            return node.id + '[@]'
        else:
            return '$' + node.id

@add_generator('Expr')
def generate_expr(self, node, ext_info):
    if isinstance(node.value, ast.Str):
        return ''  # remove line comment
    else:
        return self.dispatch(node.value)

@add_generator('List')
def generate_list(self, node, ext_info):
    for x in node.elts:
        if isinstance(x, ast.List):
            raise SyntaxNotSupportError(
                "Multiple dimension array is not support in shellscript language."
            )
    return '(%s)' % ' '.join([self.dispatch(x, ext_info) for x in node.elts])
