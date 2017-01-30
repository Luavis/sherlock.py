"""Sherlock Errors module

"""

class CompileError(Exception):
    pass

class SyntaxNotSupportError(Exception):
    pass

class ParamTypeMismatchError(Exception):
    pass

class FunctionIsNotAnalyzedError(Exception):
    def __init__(self, function_name):
        Exception.__init__(self, '%s is not analyzed', function_name)
