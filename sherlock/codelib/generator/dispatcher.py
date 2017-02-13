import ast

AST_NODE_DISPATCHER = {}


def add_generator(node_class_str=None):
    def decorator(func):
        from sherlock.codelib.generator import CodeGenerator
        global AST_NODE_DISPATCHER
        if node_class_str is not None and hasattr(ast, node_class_str):
            AST_NODE_DISPATCHER[getattr(ast, node_class_str)] = func
        setattr(CodeGenerator, func.__name__, func)
        return func
    return decorator
