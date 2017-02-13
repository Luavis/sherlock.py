import ast
from sherlock.codelib.generator.binop import generate_binop
from sherlock.errors import CompileError, SyntaxNotSupportError, FunctionIsNotAnalyzedError
from sherlock.codelib.generator.compare_op import generate_compare_op
from sherlock.codelib.generator.statement import generate_if, generate_while, generate_for

CONTEXT_STATUS_GLOBAL = 1
CONTEXT_STATUS_FUNCTION = 2

def generator_dipatcher(generator, node, ext_info={}):
    if isinstance(node, ast.Assign):
        return generator.generate_assign(node, ext_info)
    elif isinstance(node, ast.AugAssign):
        return generator.generate_aug_assign(node, ext_info)
    elif isinstance(node, ast.Name):
        return generator.generate_name(node, ext_info)
    elif isinstance(node, ast.Expr):
        return generator.generate_expr(node, ext_info)
    elif isinstance(node, ast.Call):
        return generator.generate_call(node, ext_info)
    elif isinstance(node, ast.Num):
        return generator.generate_num(node, ext_info)
    elif isinstance(node, ast.BinOp):
        return generator.generate_binop(node, ext_info)
    elif isinstance(node, ast.Str):
        return generator.generate_str(node, ext_info)
    elif isinstance(node, ast.FunctionDef):
        return generator.generate_functiondef(node, ext_info)
    elif hasattr(ast, 'arg') and isinstance(node, ast.arg):
        return generator.generate_arg(node, ext_info)
    elif isinstance(node, ast.Return):
        return generator.generate_return(node, ext_info)
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
        return generator.generate_pass(node, ext_info)
    elif isinstance(node, ast.Print):
        return generator.generate_print(node, ext_info)
    else:
        raise SyntaxNotSupportError("%s is not support yet." % node.__class__.__name__)
