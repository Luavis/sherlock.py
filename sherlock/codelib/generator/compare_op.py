import ast
from sherlock.errors import SyntaxNotSupportError


number_compare_op_table = {
    ast.Eq: '-eq',
    ast.Gt: '-gt',
    ast.GtE: '-ge',
    ast.Lt: '-lt',
    ast.LtE: '-le',
    ast.NotEq: '-ne',
    ast.Is: '-eq',
    ast.IsNot: 'ne',
}

string_compare_op_table = {
    ast.Eq: '=',
    ast.NotEq: '!',
    ast.Is: '=',
    ast.IsNot: '!',
}

def generate_compare_op(generator, node, ext_info):
    left = generator._generate(node.left, ext_info)
    right = generator._generate(node.comparators[0], ext_info)
    op_node = node.ops[0]
    left_type = generator.get_type(node.left)
    right_type = generator.get_type(node.comparators[0])

    op_code = None

    if left_type.is_number and right_type.is_number:
        op_code = number_compare_op_table.get(op_node.__class__)
    elif left_type.is_string and right_type.is_string:
        op_code = string_compare_op_table.get(op_node.__class__)

    if op_code is None:
        raise SyntaxNotSupportError('%s and %s can not compare with `%s` operator'
                % (left_type, right_type, op_node.__class__.__name__))

    return '%s %s %s' % (left, op_code, right)
