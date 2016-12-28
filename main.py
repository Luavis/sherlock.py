""" Main module.

"""
import ast
from code.generator import CodeGenerator
from code.analyzer import CodeAnalyzer


def str_node(node):
    if isinstance(node, ast.AST):
        fields = [(name, str_node(val)) for name, val in ast.iter_fields(node) if name not in ('left', 'right')]
        rv = '%s(%s' % (node.__class__.__name__, ', '.join('%s=%s' % field for field in fields))
        return rv + ')'
    else:
        return repr(node)


def main():
    code = """
a = 2 + 3
echo(a)
"""
    generator = CodeGenerator(code)
    print(generator.generate())


if __name__ == '__main__':
    main()
