from sherlock.errors import CompileError
from sherlock.codelib.generator.dispatcher import add_generator

SYSTEM_FUNCTION_TABLE = {}


def is_system_function(name):
    return name in SYSTEM_FUNCTION_TABLE.keys()

@add_generator()
def generate_system_function(generator, node, ext_info):
    function_generator = SYSTEM_FUNCTION_TABLE.get(node.func.id)
    if function_generator is None:
        raise CompileError('Function %s is not implemented.' % node.func.id)
    return function_generator(generator, node)

def system_function(name, *arg_types):
    def decorator(func):
        global SYSTEM_FUNCTION_TABLE
        def wrapper(generator, node):
            func_args = [generator, ]
            if generator is None:
                raise CompileError(
                    "Function %s is not implemented properly."
                    % func.__name__
                )

            if len(arg_types) is not len(node.args):
                raise CompileError(
                    "Function %s takes exactly %d arguments (%d given)."
                    % (func.__name__, len(arg_types), len(node.args))
                )
            for i in range(len(arg_types)):
                node_arg = node.args[i]
                if generator.get_type(node_arg) == arg_types[i]:
                    func_args.append(node_arg)
                else:
                    raise CompileError(
                        "Function %s %d-th argument must be %s type."
                        % (func.__name__, i, arg_types[i])
                    )
            return func(*func_args)
        SYSTEM_FUNCTION_TABLE[name] = wrapper
        return wrapper
    return decorator

__import__('sherlock.codelib.generator.system_function.implements')
