import ast
from sherlock.codelib.generator.dispatcher import add_generator


@add_generator('Import')
def generate_import(self, node, ext_info):
    for alias in node.names:
        raise ImportError('cannot import name %s' % alias.name)

@add_generator('ImportFrom')
def generate_from_import(self, node, ext_info):
    if node.module == 'sherlock.cmd':
        return self.generate_cmd_import(node, ext_info)
    else:
        raise ImportError('No module named %s' % node.module)
