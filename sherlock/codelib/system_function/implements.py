import ast
from sherlock.codelib.analyzer.variable import Type
from sherlock.codelib.system_function import system_function


@system_function('range', Type.LIST, Type.NUMBER, Type.NUMBER)
def system_range(g, start, end):
    return '$(seq %s $(( %s - 1 )))' % (g.dispatch(start), g.dispatch(end))

@system_function('print', Type.VOID, Type.ANY)
def system_print(g, msg):
    return 'echo %s' % g.dispatch(msg)

@system_function('pipe', Type.VOID, Type.ANY, Type.ANY)
def system_pipe(g, before, after):
    return '%s | %s' % (g.dispatch(before), g.dispatch(after))
