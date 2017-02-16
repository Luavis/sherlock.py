from sherlock.codelib.analyzer.variable import Type
from sherlock.codelib.system_function import SystemFunction
from sherlock.codelib.generator.dispatcher import add_generator


CMD_MODULE_PATH = 'sherlock.cmd'
CMD_PREFIX = '__sherlock_cmd_'
IMPORT_CMD_FORMAT = """if ! type "{cmd_name}" &> /dev/null ; then
echo "Error: Command '{cmd_name}' is not found\nplease install first"
exit 1
fi
function {prefix}{cmd_name}() {{
    export __return{prefix}{cmd_name}="$({cmd_name} $@)"
}}"""

def cmd_handler(name):
    def _handler(g, node):
        g.append_code(
            '%s%s %s' % (
                CMD_PREFIX,
                node.func.id,
                ' '.join([g.dispatch(x, {}) for x in node.args])
            )
        )
        return '__return%s%s' % (CMD_PREFIX, node.func.id)
    return _handler

def analyze_cmd(node):
    if node.module == CMD_MODULE_PATH:
        for alias in node.names:
            SystemFunction.register(
                alias.name,
                Type.STRING,
                cmd_handler(alias.name)
            )

@add_generator()
def generate_cmd_import(self, node, ext_info):
    if node.module == CMD_MODULE_PATH:
        for alias in node.names:
            self.append_code(
                IMPORT_CMD_FORMAT.format(
                    cmd_name=alias.name,
                    prefix=CMD_PREFIX,
                )
            )
