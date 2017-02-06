import ast
from sherlock.codelib.generator.binop import generate_binop
from sherlock.errors import CompileError, SyntaxNotSupportError, FunctionIsNotAnalyzedError
from sherlock.codelib.generator.compare_op import generate_compare_op

CONTEXT_STATUS_GLOBAL = 1
CONTEXT_STATUS_FUNCTION = 2

def generator_dipatcher(generator, node, ext_info={}):
    if isinstance(node, ast.Assign):
        return generator.generate_assign(node)
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
        from sherlock.codelib.generator import CodeGenerator
        function_info = generator.functions[node.name]
        if function_info is None:
            raise FunctionIsNotAnalyzedError(node.name)
        else:
            generator = CodeGenerator(
                node=node,
                context_status=CONTEXT_STATUS_FUNCTION,
                function_info=function_info,
            )
            return generator.generate()
    elif hasattr(ast, 'arg') and isinstance(node, ast.arg):
        return 'local ' + node.arg
    elif isinstance(node, ast.Return):
        return 'export __return_%s=%s' % (ext_info['func_name'], generator._generate(node.value))
    elif isinstance(node, ast.List):
        for x in node.elts:
            if isinstance(x, ast.List):
                raise SyntaxNotSupportError(
                    "Multiple dimension array is not support in shellscript language."
                )
        return '(%s)' % ' '.join([generator._generate(x, ext_info) for x in node.elts])
    elif isinstance(node, ast.If):
        test = generator._generate(node.test, ext_info)
        generator.code_buffer.append('if [ %s ]; then' % test)
        for x in node.body:
            generator.code_buffer.append(generator._generate(x))
        return 'fi'
    elif isinstance(node, ast.Compare):
        return generate_compare_op(generator, node, ext_info)
    elif isinstance(node, ast.For):
        from sherlock.codelib import str_ast_node
        print(str_ast_node(node))
        iterator = generator_dipatcher(generator, node.iter, ext_info)

        generator.code_buffer.append('for %s in %s\ndo' % (node.target.id, iterator))
        for x in node.body:
            generator.code_buffer.append(generator._generate(x))
        return 'done'
    elif isinstance(node, ast.Pass):
        return ''
    else:
        raise SyntaxNotSupportError("%s is not support yet." % node.__class__.__name__)
