
def generate_range(generator, node, ext_info):
    return '1 2 3 4 5 6'

def is_system_function(name):
    return name in SYSTEM_FUNCTION_TABLE.keys()

def generate_system_function(generator, node, ext_info):
    function_generator = SYSTEM_FUNCTION_TABLE.get(node.func.id)
    return function_generator(generator, node, ext_info)

SYSTEM_FUNCTION_TABLE = {
    'range': generate_range,
}
