import ast
from sherlock.codelib.analyzer.variable import Type
from sherlock.codelib.generator.system_function import system_function


@system_function('range', Type.NUMBER, Type.NUMBER)
def range(g, start, end):
    return '$(seq %s $(( %s - 1 )))' % (g._generate(start), g._generate(end))
