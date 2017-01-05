import ast
from sherlock.errors import CompileError, SyntaxNotSupportError


def get_node_name_with_extra_code(generator, node, extra_code):
    _ext_info = {'extra_code': extra_code}

    if isinstance(node, ast.Call):
        left_name = generator.temp_variable.get_new_name()
        _temp = '%s\n' % generator._generate(node, _ext_info)
        extra_code = '%s%s%s=$__return_%s\n' % (
            _ext_info['extra_code'],
            _temp,
            left_name,
            node.func.id,
        )
        left_name = '$%s' % left_name
    else:
        left_name = generator._generate(node, _ext_info)
        extra_code = _ext_info['extra_code']

    return left_name, extra_code

def generate_binop(generator, node, ext_info):
    left_type = generator.get_type(node.left)
    right_type = generator.get_type(node.right)
    extra_code = ext_info['extra_code']

    if left_type.is_void or right_type.is_void:
        raise CompileError('Void type is not able to operate.')

    if left_type.is_number and right_type.is_number:
        op = ''
        if isinstance(node.op, ast.Add):
            op = '+'
        elif isinstance(node.op, ast.Sub):
            op = '-'
        elif isinstance(node.op, ast.Mult):
            op = '*'
        elif isinstance(node.op, ast.Div):
            op = '/'
        else:
            raise SyntaxNotSupportError("%s operation is not support yet." % node.op.__class__.__name__)

        left_name, extra_code = get_node_name_with_extra_code(generator, node.left, extra_code)
        right_name, extra_code = get_node_name_with_extra_code(generator, node.right, extra_code)

        return '$(( %s %s %s ))' % (left_name, op, right_name), extra_code
    elif (left_type.is_string or right_type.is_string) and isinstance(node.op, ast.Add):
        _ext_info = {'extra_code': extra_code}
        left = generator._generate(node.left, _ext_info)
        right = generator._generate(node.right, _ext_info)

        return left + right, _ext_info['extra_code']
    else:
        raise SyntaxNotSupportError("%s operation is not support yet." % node.op.__class__.__name__)
