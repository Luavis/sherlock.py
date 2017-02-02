import ast
from sherlock.errors import CompileError


def generate_compare_op(generator, node, ext_info):
    left = generator._generate(node.left, ext_info)
    right = generator._generate(node.comparators[0], ext_info)
    op_node = node.ops[0]
    left_type = generator.get_type(node.left)
    right_type = generator.get_type(node.comparators[0])

    if left_type.is_number and right_type.is_number:
        if isinstance(op_node, ast.Eq):
            return '%s -eq %s' % (left, right)
        return ''
    elif left_type.is_string and right_type.is_string:
        return ''
    else:
        raise CompileError('%s can not compare with %s type'
                % (left_type, right_type))
