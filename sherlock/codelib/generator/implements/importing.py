import ast
from sherlock.codelib.generator.dispatcher import add_generator


IMPORT_CMD_FORMAT = """if ! type "%s" &> /dev/null ; then
echo "Error: Command '%s' is not found\nplease install first"
exit 1
fi"""

@add_generator('Import')
def generate_import(self, node, ext_info):
    for alias in node.names:
        raise ImportError('cannot import name %s' % alias.name)

@add_generator('ImportFrom')
def generate_from_import(self, node, ext_info):
    if node.module == 'sherlock.cmd':
        for alias in node.names:
            self.append_code(IMPORT_CMD_FORMAT % (alias.name, alias.name))
    else:
        raise ImportError('No module named %s' % node.module)
