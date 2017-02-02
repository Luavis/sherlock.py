import ast


def str_ast_node(node):
    if isinstance(node, ast.AST):
        fields = [(name, str_ast_node(val)) for name, val in ast.iter_fields(node) if name not in ('left', 'right')]
        rv = '%s(%s' % (node.__class__.__name__, ', '.join('%s=%s' % field for field in fields))
        return rv + ')'
    else:
        return repr(node)

