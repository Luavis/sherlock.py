import ast
from sherlock.codelib.generator.binop import generate_binop
from sherlock.errors import CompileError, SyntaxNotSupportError, FunctionIsNotAnalyzedError
from sherlock.codelib.generator.compare_op import generate_compare_op
from sherlock.codelib.generator.statement import generate_if, generate_while, generate_for

CONTEXT_STATUS_GLOBAL = 1
CONTEXT_STATUS_FUNCTION = 2

def generator_dipatcher(generator, node, ext_info={}):
    if isinstance(node, ast.Assign):
        return generator.generate_assign(node)
    elif isinstance(node, ast.AugAssign):
        return generator.generate_aug_assign(node, ext_info)
    elif isinstance(node, ast.Name):
        return generator.generate_name(node, ext_info.get('is_arg', False))
    elif isinstance(node, ast.Expr):
        return generator.generate_expr(node)
    elif isinstance(node, ast.Call):
        return generator.generate_call(node, ext_info)
    elif isinstance(node, ast.Num):
        return str(node.n)
    elif isinstance(node, ast.BinOp):
        if ext_info.get('extra_code') is None:
            ext_info['extra_code'] = ''

        ret, ext_info['extra_code'] = generate_binop(generator, node, ext_info)
        return ret
    elif isinstance(node, ast.Str):
        return '"' + node.s.replace('"','\\"') + '"'
    elif isinstance(node, ast.FunctionDef):
        return generator.generate_functiondef(node, ext_info)
    elif hasattr(ast, 'arg') and isinstance(node, ast.arg):
        return 'local ' + node.arg
    elif isinstance(node, ast.Return):
        return 'export __return_%s=%s' % (ext_info['func_name'], generator._generate(node.value))
    elif isinstance(node, ast.List):
        return generator.generate_list(node, ext_info)
    elif isinstance(node, ast.If):
        return generate_if(generator, node, ext_info)
    elif isinstance(node, ast.While):
        return generate_while(generator, node, ext_info)
    elif isinstance(node, ast.For):
        return generate_for(generator, node, ext_info)
    elif isinstance(node, ast.Compare):
        return generate_compare_op(generator, node, ext_info)
    elif isinstance(node, ast.Pass):
        return ''
    else:
        raise SyntaxNotSupportError("%s is not support yet." % node.__class__.__name__)
