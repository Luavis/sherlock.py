import ast
from sherlock.errors import CompileError, SyntaxNotSupportError
from sherlock.codelib.generator.dispatcher import add_generator


@add_generator('BinOp')
def generate_binop(self, node, ext_info):
    ret, ext_info['extra_code'] = _generate_binop(self, node, ext_info)
    return ret

def get_node_name_with_extra_code(self, node, extra_code):
    _ext_info = {'extra_code': extra_code}

    if isinstance(node, ast.Call):
        left_name = self.temp_variable.get_new_name()
        _temp = '%s\n' % self.dispatch(node, _ext_info)
        extra_code = '%s%s%s=$__return_%s\n' % (
            _ext_info['extra_code'],
            _temp,
            left_name,
            node.func.id,
        )
        left_name = '$%s' % left_name
    else:
        left_name = self.dispatch(node, _ext_info)
        extra_code = _ext_info['extra_code']

    return left_name, extra_code

def _generate_binop(self, node, ext_info):
    left_type = self.get_type(node.left)
    right_type = self.get_type(node.right)
    extra_code = ext_info.get('extra_code', '')

    if left_type.is_void or right_type.is_void:
        raise CompileError('Void type is not able to operate.')

    if left_type.is_number and right_type.is_number:
        op = self.generate_numeric_op(node.op, ext_info)
        if len(op) is 0:
            raise SyntaxNotSupportError("%s operation is not support yet." % node.op.__class__.__name__)

        left_name, extra_code = get_node_name_with_extra_code(self, node.left, extra_code)
        right_name, extra_code = get_node_name_with_extra_code(self, node.right, extra_code)

        return '$(( %s %s %s ))' % (left_name, op, right_name), extra_code
    elif (left_type.is_string or right_type.is_string) and isinstance(node.op, ast.Add):
        _ext_info = {'extra_code': extra_code}
        left = self.dispatch(node.left, _ext_info)
        right = self.dispatch(node.right, _ext_info)

        return left + right, _ext_info['extra_code']
    else:
        raise SyntaxNotSupportError("%s operation is not support yet." % node.op.__class__.__name__)

