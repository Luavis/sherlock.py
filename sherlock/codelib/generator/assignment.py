import ast
from sherlock.errors import CompileError, SyntaxNotSupportError
from sherlock.codelib.generator.dispatcher import add_generator


@add_generator('Assign')
def generate_assign(self, node, ext_info):
    target_code = ''
    if isinstance(node.targets[0], ast.Name):
        target_code = self.dispatch(node.targets[0])
    else:
        raise CompileError()

    if isinstance(node.value, ast.Call):
        return '%s\n%s=$__return_%s' % (
            self.dispatch(node.value),
            target_code,
            node.value.func.id
        )
    else:
        ext_info = {}
        value_code = self.dispatch(node.value, ext_info)
        extra_code = ext_info.get('extra_code', '')
        if value_code is None:
            raise CompileError()

        return extra_code + target_code + '=' + value_code

@add_generator('AugAssign')
def generate_aug_assign(self, node, ext_info):
    tmp_name = self.temp_variable.get_new_name()
    tmp_assign_code = '%s=%s' % (
        tmp_name,
        self.dispatch(node.value)
    )
    self.code_buffer.append(tmp_assign_code)
    target = self.dispatch(node.target)
    target_type = self.get_type(node.target)
    if target_type.is_number:
        op = self.generate_numeric_op(node.op, ext_info)
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
